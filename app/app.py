"""
Dongo HelpDesk - Aplicación principal / Main application module
---------------------------------------------------------------

Proyecto:
    Dongo HelpDesk

Descripción:
    Módulo principal que define las rutas HTTP, validaciones, y eventos en tiempo real
    (Socket.IO) para el sistema de mesa de ayuda. Contiene autenticación básica,
    CRUD de tickets, vistas de dashboard y chat (público y privado).

    Main module that defines HTTP routes, validations, and real-time events
    (Socket.IO) for the help desk system. Contains basic authentication,
    ticket CRUD, dashboard views and chat (public and private).

Autores:
    Miguel Angel Leon Leon

Tecnologías:
    - Flask
    - Flask-SocketIO
    - SQLAlchemy (ORM)
    - Python 3.x

Notas:
    - Este archivo asume que el módulo `models` provee: sesion, Usuarios, Tickets,
      RespuestasTickets, Mensajes (modelos SQLAlchemy).
    - Las docstrings están en estilo Google para compatibilidad con Sphinx + napoleon.

    This file assumes that the `models` module provides: sesion, Usuarios, Tickets,
    RespuestasTickets, Mensajes (SQLAlchemy models).
    Docstrings use Google style for compatibility with Sphinx + napoleon.
"""

import re
from flask import Flask, render_template, redirect, session, url_for, request, flash, send_from_directory
from flask_socketio import SocketIO, send, emit, join_room
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models import sesion, Usuarios, Tickets, RespuestasTickets, Mensajes, Roles
from flask_babel import Babel, gettext as _

# -----------------------------
# Configuración de la app
# -----------------------------
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
rooms = {}  #: Diccionario temporal para mapear username -> room en memoria (no persistente).
app.secret_key = 'p4ssw0rd_hyp4r_s4cUr4'  #: Clave de sesión (reemplazar en producción).

# Configuración de Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# ============================
#  VALIDACIONES (regex)
# ============================
#: Expresión regular para validar nombres de usuario (4–20 caracteres alfanuméricos o guión bajo).
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_]{4,20}$')

#: Expresión regular para validar contraseñas (mínimo 6 caracteres, con letras y números).
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@#$*%^&+=!]{6,20}$')

#: Expresión regular para correos electrónicos.
EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$')

#: Expresión regular para nombres (incluye acentos y ñ).
NAME_REGEX = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]{2,30}$')

#: Expresión regular para números de documento (6 a 12 dígitos).
DOC_REGEX = re.compile(r'^\d{6,12}$')

# ============================
#  IDIOMA / BABEL
# ============================

# 📘 Inicializar Babel con función de idioma
def get_locale():
    return session.get('lang', 'es')

babel = Babel(app, locale_selector=get_locale)

# 🔹 Registrar función para Jinja
app.jinja_env.globals['get_locale'] = get_locale

# 📘 Ruta para cambiar idioma
@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    session['lang'] = lang_code
    return redirect(request.referrer or url_for('dashboard_admin'))

# ============================
#  RUTAS PÚBLICAS / AUTH
# ============================

@app.route('/')
def index():
    """
    Redirige a la página de login.
    Redirects to the login page.

    Returns:
        werkzeug Response: Redirección a la ruta 'login'.

    Notes:
        Ruta raíz que simplemente envía a /login.
    """
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Maneja la pantalla de inicio de sesión y la autenticación de usuarios.

    Spanish:
        - Si el método es GET, renderiza el template 'login.html'.
        - Si el método es POST, valida username/password con regex y consulta la BD.
        - Si es válido, guarda información en la sesión y redirige según el rol.

    English:
        - GET renders 'login.html'.
        - POST validates username/password via regex and queries DB.
        - On success, stores session info and redirects according to user role.

    Returns:
        Response: render_template('login.html') o redirect a dashboard según rol.
    """
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Validaciones rápidas
        if not USERNAME_REGEX.match(username):
            flash('Usuario o contraseña incorrecto', 'error')
            return render_template('login.html')

        if not PASSWORD_REGEX.match(password):
            flash('Usuario o contraseña incorrecto', 'error')
            return render_template('login.html')

        # Consulta en la base de datos
        usuario = sesion.query(Usuarios).filter(
            Usuarios.username == username, Usuarios.contrasena == password
        ).first()

        if usuario:
            # Guardar en sesión datos mínimos
            session['usuario'] = usuario.username
            session['user_id'] = usuario.id
            session['rol'] = usuario.rol.tipo_rol

            # Redirección según rol
            if usuario.rol.tipo_rol == 'Administrador':
                return redirect(url_for('dashboard_admin'))
            elif usuario.rol.tipo_rol == 'Soporte':
                return redirect(url_for('dashboard_soporte'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')

    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """
    Permite a un usuario solicitar recuperación de contraseña.

    - Crea un ticket automático para el área de soporte.
    - El ticket se marca como prioridad alta.
    """
    if request.method == 'POST':
        nombre = request.form['nombre_completo']
        cedula = request.form['cedula']
        correo = request.form['correo']

        # Crear ticket automático
        nuevo_ticket = Tickets(
            titulo=f"Recuperación de contraseña - {nombre}",
            descripcion=f"Solicitud de recuperación de acceso.\nNombre: {nombre}\nCédula: {cedula}\nCorreo: {correo}",
            categoria="Soporte",
            prioridad="Alta",
            estado="Abierto",
            fecha_creacion=datetime.now()
        )

        sesion.add(nuevo_ticket)
        sesion.commit()

        flash("Tu solicitud ha sido enviada correctamente. El área de soporte te contactará por correo.", "success")
        return redirect(url_for('login'))

    return render_template('forgot_password.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            tipo_documento = request.form.get('tipo_de_documento')
            numero_documento = request.form.get('numberd', '').strip()

            primer_nombre = request.form.get('primer_nombre', '').strip()
            segundo_nombre = request.form.get('segundo_nombre', '').strip()
            primer_apellido = request.form.get('primer_apellido', '').strip()
            segundo_apellido = request.form.get('segundo_apellido', '').strip()

            username = request.form.get('username', '').strip()
            correo = request.form.get('correo', '').strip()
            password = request.form.get('password', '').strip()

            # Validaciones
            if not DOC_REGEX.match(numero_documento):
                flash('Número de documento inválido', 'error')
                return render_template('register.html')

            if not NAME_REGEX.match(primer_nombre) or not NAME_REGEX.match(primer_apellido):
                flash('Nombre o apellido inválidos', 'error')
                return render_template('register.html')

            if segundo_nombre and not NAME_REGEX.match(segundo_nombre):
                flash('Segundo nombre inválido', 'error')
                return render_template('register.html')

            if segundo_apellido and not NAME_REGEX.match(segundo_apellido):
                flash('Segundo apellido inválido', 'error')
                return render_template('register.html')

            if not USERNAME_REGEX.match(username):
                flash('Usuario inválido', 'error')
                return render_template('register.html')

            if not EMAIL_REGEX.match(correo):
                flash('Correo inválido', 'error')
                return render_template('register.html')

            if not PASSWORD_REGEX.match(password):
                flash('Contraseña inválida', 'error')
                return render_template('register.html')

            # Crear usuario
            usuario = Usuarios(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                primer_nombre=primer_nombre,
                segundo_nombre=segundo_nombre,
                primer_apellido=primer_apellido,
                segundo_apellido=segundo_apellido,
                username=username,
                correo=correo,
                contrasena=password,
                rol_id=1
            )

            sesion.add(usuario)
            sesion.commit()

            flash('Registro exitoso', 'success')
            return redirect(url_for('login'))

        except IntegrityError as e:
            sesion.rollback()
            msg = str(e.orig).lower()

            if "numero_documento" in msg:
                flash('Documento ya registrado', 'error')
            elif "username" in msg:
                flash('Usuario ya existe', 'error')
            elif "correo" in msg:
                flash('Correo ya registrado', 'error')
            else:
                flash('Error en el registro', 'error')

    return render_template('register.html')

@app.route('/logout')
def logout():
    """
    Limpia la sesión del usuario y redirige a la página de login.

    English:
        Clears the user's session and redirects to the login page.

    Returns:
        Response: redirect a 'login'
    """
    session.clear()
    return redirect(url_for('login'))


# ============================
#  DASHBOARDS Y PERFIL
# ============================

@app.route('/dashboard')
def dashboard():
    """
    Dashboard principal para usuarios regulares.

    Spanish:
        - Requiere que exista 'user_id' en sesión.
        - Obtiene estadísticas de tickets del usuario y la lista de sus tickets.

    English:
        - Requires 'user_id' in session.
        - Retrieves ticket stats and list for the user.

    Returns:
        Response: render_template('dashboard.html', ...)
    """
    if 'user_id' in session:
        user_id = session.get('user_id')
        name = sesion.query(Usuarios).filter(Usuarios.id == user_id).first()
        nombre = name.primer_nombre if name else 'Invitado'

        abiertos = sesion.query(Tickets).filter(Tickets.usuario_id == user_id, Tickets.estado == 'Abierto').count()
        progreso = sesion.query(Tickets).filter(Tickets.usuario_id == user_id, Tickets.estado == 'En progreso').count()
        cerrados = sesion.query(Tickets).filter(Tickets.usuario_id == user_id, Tickets.estado == 'Cerrado').count()

        tickets = sesion.query(Tickets).filter(Tickets.usuario_id == user_id).all()
        return render_template(
            'dashboard.html',
            tickets=tickets,
            abiertos=abiertos,
            progreso=progreso,
            cerrados=cerrados,
            nombre=nombre
        )
    else:
        return redirect(url_for('login'))


@app.route('/dashboard_admin')
def dashboard_admin():
    """
    Dashboard para administradores.

    Spanish:
        - Muestra usuarios, tickets y estadísticas globales.
    English:
        - Shows users, tickets and overall statistics.

    Returns:
        Response: render_template('dashboard_admin.html', ...)
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    usuarios = sesion.query(Usuarios).all()
    total_usuarios = len(usuarios)

    tickets = sesion.query(Tickets).all()
    tickets_abiertos = sesion.query(Tickets).filter_by(estado="Abierto").count()
    tickets_progreso = sesion.query(Tickets).filter_by(estado="En progreso").count()
    tickets_cerrados = sesion.query(Tickets).filter_by(estado="Cerrado").count()

    return render_template(
        "dashboard_admin.html",
        usuarios=usuarios,
        tickets=tickets,
        total_usuarios=total_usuarios,
        tickets_abiertos=tickets_abiertos,
        tickets_progreso=tickets_progreso,
        tickets_cerrados=tickets_cerrados
    )


@app.route('/perfil')
def perfil():
    """
    Muestra el perfil del usuario actual.

    Spanish:
        - Construye nombre completo, correo, documento y rol para mostrar.
    English:
        - Builds full name, email, document and role to display.

    Returns:
        Response: render_template('perfil.html', ...)
    """
    if 'user_id' in session:
        user_id = session.get('user_id')
        usuario = sesion.query(Usuarios).filter(Usuarios.id == user_id).first()

        nombre = f'{usuario.primer_nombre} {usuario.primer_apellido} {usuario.segundo_apellido}' if usuario else 'Invitado'
        correo = usuario.correo if usuario and usuario.correo else 'No tiene correo'
        documento = f'{usuario.tipo_documento} - {usuario.numero_documento}' if usuario and usuario.tipo_documento and usuario.numero_documento else 'N/A'
        rol = usuario.rol.tipo_rol if usuario and usuario.rol else 'Invitado'

        return render_template('perfil.html', nombre=nombre, correo=correo, documento=documento, rol=rol)

    return redirect(url_for('login'))


@app.route('/perfil_admin')
def perfil_admin():
    """
    Muestra perfil del administrador actualmente autenticado.

    English:
        Shows the current authenticated administrator profile.

    Returns:
        Response: render_template('perfil_admin.html', ...)
    """
    if 'user_id' in session:
        user_id = session.get('user_id')
        usuario = sesion.query(Usuarios).filter(Usuarios.id == user_id).first()

        nombre = f'{usuario.primer_nombre} {usuario.primer_apellido} {usuario.segundo_apellido}' if usuario else 'Invitado'
        correo = usuario.correo if usuario and usuario.correo else 'No tiene correo'
        documento = f'{usuario.tipo_documento} - {usuario.numero_documento}' if usuario and usuario.tipo_documento and usuario.numero_documento else 'N/A'
        rol = usuario.rol.tipo_rol if usuario and usuario.rol else 'Invitado'

        return render_template('perfil_admin.html', nombre=nombre, correo=correo, documento=documento, rol=rol)

    return redirect(url_for('login'))

@app.route('/dashboard_soporte')
def dashboard_soporte():
    """
    Dashboard para el personal de soporte.

    Spanish:
        - Muestra tickets con categoría 'Soporte'.
    English:
        - Shows tickets in the 'Soporte' category.
    """

    # Verifica que haya una sesión activa
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Obtiene el usuario actual
    usuario = sesion.query(Usuarios).filter_by(id=session['user_id']).first()

    # Solo permite acceso si el rol es soporte
    if usuario.rol.tipo_rol.lower() != "soporte":
        flash("Acceso no autorizado", "error")
        return redirect(url_for('inicio'))
    
    # Filtrar tickets solo con categoría 'Soporte'
    tickets_soporte = sesion.query(Tickets).filter_by(categoria='Soporte Tecnico').all()

    # Contar por estado
    tickets_abiertos = sesion.query(Tickets).filter_by(categoria='Soporte Tecnico', estado='Abierto').count()
    tickets_progreso = sesion.query(Tickets).filter_by(categoria='Soporte Tecnico', estado='En progreso').count()
    tickets_cerrados = sesion.query(Tickets).filter_by(categoria='Soporte Tecnico', estado='Cerrado').count()

    return render_template(
        'dashboard_soporte.html',
        usuario=usuario,
        tickets=tickets_soporte,
        tickets_abiertos=tickets_abiertos,
        tickets_progreso=tickets_progreso,
        tickets_cerrados=tickets_cerrados
    )

@app.route('/gestion_tickets_soporte')
def gestion_tickets_soporte():
    """
    Gestión de tickets para el rol Soporte.
    Solo muestra tickets de categoría 'Soporte' o 'Soporte Técnico'.
    """

    if 'user_id' not in session:
        return redirect(url_for('login'))

    usuario = sesion.query(Usuarios).filter_by(id=session['user_id']).first()

    if usuario.rol.tipo_rol.lower() != "soporte":
        flash("Acceso no autorizado", "error")
        return redirect(url_for('inicio'))

    # Obtener filtros de estado
    estado = request.args.get('estado')

    query = sesion.query(Tickets).filter(
        (Tickets.categoria == 'Soporte') | (Tickets.categoria == 'Soporte Técnico')
    )

    if estado:
        query = query.filter_by(estado=estado)

    tickets = query.all()

    # Contar por estado
    tickets_abiertos = sesion.query(Tickets).filter_by(categoria='Soporte', estado='Abierto').count()
    tickets_progreso = sesion.query(Tickets).filter_by(categoria='Soporte', estado='En progreso').count()
    tickets_cerrados = sesion.query(Tickets).filter_by(categoria='Soporte', estado='Cerrado').count()

    return render_template(
        'gestion_tickets_soporte.html',
        usuario=usuario,
        tickets=tickets,
        estado=estado,
        tickets_abiertos=tickets_abiertos,
        tickets_progreso=tickets_progreso,
        tickets_cerrados=tickets_cerrados
    )

@app.route('/perfil_soporte')
def perfil_soporte():
    """
    Muestra perfil del soporte actualmente autenticado.

    English:
        Shows the current authenticated support profile.

    Returns:
        Response: render_template('perfil_soporte.html', ...)
    """
    if 'user_id' in session:
        user_id = session.get('user_id')
        usuario = sesion.query(Usuarios).filter(Usuarios.id == user_id).first()

        nombre = f'{usuario.primer_nombre} {usuario.primer_apellido} {usuario.segundo_apellido}' if usuario else 'Invitado'
        correo = usuario.correo if usuario and usuario.correo else 'No tiene correo'
        documento = f'{usuario.tipo_documento} - {usuario.numero_documento}' if usuario and usuario.tipo_documento and usuario.numero_documento else 'N/A'
        rol = usuario.rol.tipo_rol if usuario and usuario.rol else 'Invitado'

        return render_template('perfil_soporte.html', nombre=nombre, correo=correo, documento=documento, rol=rol)

    return redirect(url_for('login'))

# ============================
#  TICKETS (crear, ver, cerrar)
# ============================

@app.route('/crear_ticket', methods=['GET', 'POST'])
def crear_ticket():
    """
    Crea un nuevo ticket para el usuario autenticado.
    """
    if 'user_id' in session:
        user_id = session.get('user_id')
        if request.method == 'POST':
            titulo = request.form.get('titulo', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            categoria = request.form.get('categoria')
            prioridad = request.form.get('prioridad')

            if not titulo or not descripcion:
                flash('El título y la descripción son obligatorios.', 'error')
                return render_template('crear_ticket.html')

            ticket = Tickets(
                titulo=titulo,
                descripcion=descripcion,
                categoria=categoria,
                prioridad=prioridad,
                usuario_id=user_id
            )

            sesion.add(ticket)
            sesion.commit()

            flash('¡Se ha enviado tu ticket!', 'alert')
            return redirect(url_for('dashboard'))

        return render_template('crear_ticket.html')

    return redirect(url_for('login'))


@app.route('/ver_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def ver_ticket(ticket_id):
    """
    Vista detallada de un ticket. Permite cambiar estado/prioridad y agregar respuestas.
    Compatible con Admin y Soporte.
    """
    if 'user_id' not in session or session.get('rol') not in ['Administrador', 'Soporte', 'Usuario']:
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('login'))

    ticket = sesion.query(Tickets).filter_by(id=ticket_id).first()
    if not ticket:
        flash('El ticket no existe o fue eliminado.', 'error')
        if session.get('rol') == 'Administrador':
            return redirect(url_for('gestion_tickets'))
        elif session.get('rol') == 'Soporte':
            return redirect(url_for('gestion_tickets_soporte'))
        else:
            return redirect(url_for('dashboard'))

    if request.method == 'POST':
        nuevo_estado = request.form.get('estado')
        nueva_prioridad = request.form.get('prioridad')
        respuesta_texto = request.form.get('respuesta')

        # Actualizar estado y prioridad (solo admin/soporte)
        if session.get('rol') in ['Administrador', 'Soporte']:
            if nuevo_estado:
                ticket.estado = nuevo_estado
            if nueva_prioridad:
                ticket.prioridad = nueva_prioridad

        # Agregar respuesta
        if respuesta_texto:
            nueva_respuesta = RespuestasTickets(
                ticket_id=ticket.id,
                usuario_id=session['user_id'],
                mensaje=respuesta_texto
            )
            sesion.add(nueva_respuesta)

        sesion.commit()
        flash('Cambios guardados correctamente.', 'success')

        # Redirigir según el rol
        if session.get('rol') == 'Administrador':
            return redirect(url_for('gestion_tickets'))
        elif session.get('rol') == 'Soporte':
            return redirect(url_for('gestion_tickets_soporte'))
        else:
            return redirect(url_for('dashboard'))

    respuestas = sesion.query(RespuestasTickets).filter_by(ticket_id=ticket.id).all()
    return render_template('ver_ticket.html', ticket=ticket, respuestas=respuestas)


@app.route('/cerrar_ticket/<int:ticket_id>')
def cerrar_ticket(ticket_id):
    """
    Cambia el estado del ticket a 'Cerrado' y registra la fecha de solución.
    Compatible con Admin y Soporte.
    """
    if 'user_id' not in session or session.get('rol') not in ['Administrador', 'Soporte']:
        flash("No tienes permisos para cerrar tickets.", "error")
        return redirect(url_for('login'))

    ticket = sesion.query(Tickets).filter_by(id=ticket_id).first()
    if ticket:
        ticket.estado = 'Cerrado'
        ticket.fecha_solucion = datetime.now()
        sesion.commit()
        flash('Ticket cerrado correctamente.', 'success')
    else:
        flash('No se encontró el ticket.', 'error')

    if session.get('rol') == 'Administrador':
        return redirect(url_for('gestion_tickets'))
    elif session.get('rol') == 'Soporte':
        return redirect(url_for('gestion_tickets_soporte'))
    else:
        return redirect(url_for('dashboard'))


@app.route('/usuario/ticket/<int:ticket_id>')
def ver_ticket_usuario(ticket_id):
    """
    Vista pública/usuario que muestra un ticket y sus respuestas ordenadas cronológicamente.
    """
    ticket = sesion.query(Tickets).filter_by(id=ticket_id).first()
    if not ticket:
        return "Ticket no encontrado", 404

    respuestas = (
        sesion.query(RespuestasTickets)
        .filter_by(ticket_id=ticket_id)
        .order_by(RespuestasTickets.fecha_respuesta.asc())
        .all()
    )
    return render_template('ver_ticket_usuario.html', ticket=ticket, respuestas=respuestas)

@app.route('/gestion_tickets')
def gestion_tickets():
    """
    Listado y gestión de tickets con filtros opcionales.

    Query params:
        - estado: filtra por estado del ticket (e.g., 'Abierto')
        - categoria: filtra por categoría

    Returns:
        Response: render_template('gestion_tickets.html', ...) con listas y estadísticas.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    estado = request.args.get('estado')
    categoria = request.args.get('categoria')

    query = sesion.query(Tickets)

    if estado:
        query = query.filter(Tickets.estado == estado)
    if categoria:
        query = query.filter(Tickets.categoria == categoria)

    tickets = query.order_by(Tickets.fecha_creacion.desc()).all()
    usuarios = sesion.query(Usuarios).all()

    total_usuarios = sesion.query(Usuarios).count()
    tickets_abiertos = sesion.query(Tickets).filter(Tickets.estado == "Abierto").count()
    tickets_progreso = sesion.query(Tickets).filter(Tickets.estado == "En progreso").count()
    tickets_cerrados = sesion.query(Tickets).filter(Tickets.estado == "Cerrado").count()

    return render_template(
        'gestion_tickets.html',
        usuarios=usuarios,
        tickets=tickets,
        total_usuarios=total_usuarios,
        tickets_abiertos=tickets_abiertos,
        tickets_progreso=tickets_progreso,
        tickets_cerrados=tickets_cerrados,
        estado=estado,
        categoria=categoria
    )

@app.route('/responder_ticket_soporte/<int:ticket_id>', methods=['GET', 'POST'])
def responder_ticket_soporte(ticket_id):
    if 'user_id' not in session or session.get('rol') != 'Soporte':
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('login'))

    ticket = sesion.query(Tickets).filter_by(id=ticket_id).first()
    if not ticket:
        flash('El ticket no existe.', 'error')
        return redirect(url_for('gestion_tickets_soporte'))

    if request.method == 'POST':
        mensaje = request.form.get('mensaje')
        if mensaje:
            respuesta = RespuestasTickets(
                ticket_id=ticket.id,
                usuario_id=session['user_id'],
                mensaje=mensaje
            )
            sesion.add(respuesta)
            sesion.commit()
            flash('Respuesta enviada correctamente.', 'success')
            return redirect(url_for('ver_ticket', ticket_id=ticket.id))

    return render_template('responder_ticket_soporte.html', ticket=ticket)

# ============================
#  CHAT (general/admin + privado persistente)
# ============================

@app.route('/chat_admin')
def chat_admin():
    """
    Vista para el chat general o sala de admin según rol.

    English:
        Renders a chat template and define which room usar (sala_general o sala_admin).

    Returns:
        Response: render_template('chat_admin.html', username=username, room=room, rol=rol)
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    username = session.get('usuario')
    rol = session.get('rol')
    room = 'sala_general' if rol != 'Administrador' else 'sala_admin'
    return render_template('chat_admin.html', username=username, room=room, rol=rol)


@app.route('/chat_privado')
def lista_chats():
    """
    Lista de usuarios para iniciar un chat privado.

    English:
        Returns a list of other users (excludes current user) to start private chats.

    Returns:
        Response: render_template('lista_chats.html', usuarios=usuarios)
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    usuarios = sesion.query(Usuarios).filter(Usuarios.id != user_id).all()

    return render_template('lista_chats.html', usuarios=usuarios)


@app.route('/chat/<int:receiver_id>')
def chat_privado(receiver_id):
    """
    Muestra la conversación privada entre el usuario en sesión y otro usuario.

    Args:
        receiver_id (int): ID del usuario receptor.

    Returns:
        Response: render_template('chat_privado.html', mensajes=mensajes, receiver=receiver)
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    mensajes = (
        sesion.query(Mensajes)
        .filter(
            ((Mensajes.sender_id == user_id) & (Mensajes.receiver_id == receiver_id)) |
            ((Mensajes.sender_id == receiver_id) & (Mensajes.receiver_id == user_id))
        )
        .order_by(Mensajes.fecha_envio.asc())
        .all()
    )
    receiver = sesion.query(Usuarios).filter_by(id=receiver_id).first()
    return render_template('chat_privado_usuario.html', mensajes=mensajes, receiver=receiver)


# ============================
#  SOCKET.IO - Eventos
# ============================

@socketio.on('join')
def handle_join(data):
    """
    Evento Socket.IO: 'join'
    - El usuario se une a una sala pública o de admin.
    - Mapea username -> room en memoria y emite un mensaje de notificación.

    Args:
        data (dict): { 'username': str, 'room': str }

    English:
        Socket.IO 'join' event for joining public/admin room.

    Returns:
        None: Emite un evento 'message' al room.
    """
    username = data.get('username')
    room = data.get('room')
    if room:
        join_room(room)
        rooms[username] = room
        emit('message', {'msg': f"🟢 {username} se ha unido al chat."}, room=room)


@socketio.on('message')
def handle_message(data):
    """
    Evento Socket.IO: 'message'
    - Envía mensajes a la sala indicada (no persiste en BD).

    Args:
        data (dict): { 'username': str, 'msg': str, 'room': str }

    English:
        Sends a chat message to the specified room. Timestamped on server.

    Returns:
        None: Usa send(...) para enviar a la sala.
    """
    username = data.get('username')
    msg = data.get('msg')
    room = data.get('room')
    hora = datetime.now().strftime("%H:%M:%S")
    mensaje = f"[{hora}] {username}: {msg}"
    if room:
        send({'msg': mensaje}, room=room)


@socketio.on('disconnect')
def handle_disconnect():
    """
    Evento Socket.IO: 'disconnect'
    - Notifica que un usuario salió del chat y elimina su mapeo en memoria.

    English:
        Notifies rooms that a user disconnected and removes them from the in-memory map.

    Returns:
        None
    """
    for user, room in list(rooms.items()):
        emit('message', {'msg': f"🔴 {user} salió del chat."}, room=room)
        # Elimina la primera coincidencia y rompe para evitar modificar dict durante iteración
        del rooms[user]
        break


@socketio.on('join_private')
def handle_join_private(data):
    """
    Evento Socket.IO: 'join_private'
    - Permite a dos usuarios unirse a una sala privada calculada por sus IDs.

    Args:
        data (dict): { 'user_id': int, 'target_id': int }

    Returns:
        None: realiza join_room a la sala privada y emite un mensaje.
    """
    user_id = data.get('user_id')
    target_id = data.get('target_id')
    if user_id is None or target_id is None:
        return
    room = f"chat_{min(user_id, target_id)}_{max(user_id, target_id)}"
    join_room(room)
    emit('message', {'msg': f"🟢 Se unió al chat."}, room=room)


@socketio.on('private_message')
def handle_private_message(data):
    """
    Evento Socket.IO: 'private_message'
    - Guarda el mensaje privado en la base de datos y lo envía a la sala privada.

    Args:
        data (dict): { 'sender_id': int, 'receiver_id': int, 'msg': str }

    English:
        Persists the private message and broadcasts it to the private chat room.

    Returns:
        None
    """
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    msg = data.get('msg')
    if sender_id is None or receiver_id is None or not msg:
        return

    hora = datetime.now().strftime("%H:%M")

    # Guardar en BD
    nuevo_mensaje = Mensajes(
        sender_id=sender_id,
        receiver_id=receiver_id,
        contenido=msg
    )
    sesion.add(nuevo_mensaje)
    sesion.commit()

    room = f"chat_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
    send({
        'msg': f"[{hora}] {msg}",
        'sender_id': sender_id
    }, room=room)

# ============================
#  REPORTES ADMIN
# ============================

from io import BytesIO
import pandas as pd
from flask import send_file

@app.route('/reportes', methods=['GET', 'POST'])
def reportes():
    """
    Página de reportes administrativos.
    Permite filtrar tickets y usuarios, y exportar la información.
    """
    if 'rol' not in session or session['rol'] != 'Administrador':
        flash("Acceso no autorizado.", "error")
        return redirect(url_for('login'))

    filtros = {}
    resultados = []

    if request.method == 'POST':
        tipo = request.form.get('tipo')
        estado = request.form.get('estado')
        prioridad = request.form.get('prioridad')

        if tipo == 'tickets':
            query = sesion.query(Tickets).join(Usuarios)

            if estado:
                query = query.filter(Tickets.estado == estado)
            if prioridad:
                query = query.filter(Tickets.prioridad == prioridad)

            resultados = query.all()
            filtros['tipo'] = 'tickets'

        elif tipo == 'usuarios':
            query = sesion.query(Usuarios).join(Roles)
            rol = request.form.get('rol')
            if rol:
                query = query.filter(Roles.tipo_rol == rol)
            resultados = query.all()
            filtros['tipo'] = 'usuarios'

    return render_template('reportes.html', resultados=resultados, filtros=filtros)

# ============================
#  RUN
# ============================
if __name__ == '__main__':
    """
    Punto de entrada principal del servidor Flask.

    English:
        Main entry point for the Flask + Socket.IO server.
    """
    socketio.run(app, port=5860, debug=True, host='0.0.0.0')