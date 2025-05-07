from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
import datetime

engine = create_engine('mysql+pymysql://root:desulek@localhost:3306/db_mesa_de_ayuda')

def verificar(nombre_usuario, contraseña):

    """
    Verifica las credenciales del usuario.

    Esta función consulta la base de datos para verificar si el nombre de usuario y 
    la contraseña proporcionada coinciden con los registros almacenados. Si la verificación es exitosa, 
    devuelve el id del usuario y su rol.

    Args:
        nombre_usuario (str): El nombre de usuario a verificar.
        contraseña (str): La contraseña asociada al nombre de usuario.

    Returns:
        tuple: Un par con el id del usuario y su rol si la verificación es exitosa, 
               o (None, None) si no se encuentran registros que coincidan.
    """

    with engine.connect() as conexion:
        query = text("""
            SELECT c.id_usuario, c.rol
            FROM credenciales c
            WHERE c.nombre_usuario = :nombre_usuario AND c.contraseña_hash = :contraseña
        """)
        result = conexion.execute(query, {'nombre_usuario': nombre_usuario, 'contraseña': contraseña}).fetchone()
        
        # Si result no es None, retornar el id_usuario y el rol
        if result is not None:
            id_usuario = result[0]  # id_usuario
            rol = result[1]  # rol (por ejemplo: 'administrador' o 'usuario')
            return id_usuario, rol
        
        return None, None  # Si no se encuentra el usuario o la contraseña
    
def registrar(nombre, segundo_nombre, apellido, segundo_apellido, tipo_id, numero_identificacion, fecha_registro, correo, contraseña_hash, telefono_principal, telefono_secundario, fecha_actualizacion, nombre_usuario):

    """
    Registra un nuevo usuario y sus credenciales.

    Esta función realiza dos inserciones en la base de datos: una para los datos del usuario 
    y otra para las credenciales. Si ambas inserciones son exitosas, se confirma el registro.

    Args:
        nombre (str): Nombre del usuario.
        segundo_nombre (str): Segundo nombre del usuario.
        apellido (str): Apellido del usuario.
        segundo_apellido (str): Segundo apellido del usuario.
        tipo_id (str): Tipo de identificación (por ejemplo, "Cédula").
        numero_identificacion (str): Número de identificación del usuario.
        fecha_registro (datetime): Fecha en la que el usuario se registra.
        correo (str): Correo electrónico del usuario.
        contraseña_hash (str): Contraseña en formato hash.
        telefono_principal (str): Teléfono principal del usuario.
        telefono_secundario (str): Teléfono secundario del usuario (opcional).
        fecha_actualizacion (datetime): Fecha de la última actualización de las credenciales.
        nombre_usuario (str): Nombre de usuario para el acceso.

    Returns:
        bool: True si el registro fue exitoso, False en caso de error.
    """

    try:
        with engine.begin() as conexion:
            query_usuarios = text("""INSERT INTO usuarios (nombre, segundo_nombre, apellido, segundo_apellido, tipo_identificacion, numero_identificacion, fecha_registro)
                        VALUES (:nombre, :segundo_nombre, :apellido, :segundo_apellido, :tipo_id, :numero_identificacion, :fecha_registro)""")
            result = conexion.execute(query_usuarios, {'nombre': nombre,
                                    'segundo_nombre': segundo_nombre,
                                    'apellido': apellido,
                                    'segundo_apellido': segundo_apellido,
                                    'tipo_id': tipo_id,
                                    'numero_identificacion': numero_identificacion,
                                    'fecha_registro': fecha_registro})
            conexion.commit()

            id_usuario = result.lastrowid

            query_credenciales = text("""INSERT INTO credenciales (id_usuario, correo, contraseña_hash, telefono_principal, telefono_secundario, fecha_actualizacion, nombre_usuario)
                                      VALUES (:id_usuario, :correo, :contraseña_hash, :telefono_principal, :telefono_secundario, :fecha_actualizacion, :nombre_usuario)""")
            conexion.execute(query_credenciales, {'id_usuario': id_usuario,
                                                  'correo': correo,
                                                  'contraseña_hash': contraseña_hash,
                                                  'telefono_principal': telefono_principal,
                                                  'telefono_secundario': telefono_secundario,
                                                  'fecha_actualizacion': fecha_actualizacion,
                                                  'nombre_usuario': nombre_usuario})
            conexion.commit()

            return True
    except Exception as e:
        print('Error al registrar:', e)
        return False

def obtener_datos_usuario(id_usuario):

    """
    Obtiene los datos personales de un usuario.

    Esta función consulta la base de datos para obtener los datos del usuario, incluyendo 
    su nombre, apellidos, tipo de identificación, y datos de contacto (correo, teléfonos).

    Args:
        id_usuario (int): El id del usuario cuya información se desea obtener.

    Returns:
        tuple: Una tupla con los datos del usuario (nombre, segundo nombre, apellido, etc.), o None si no se encuentra.
    """

    with Session(engine) as session:
        query = text("""
            SELECT u.nombre, u.segundo_nombre, u.apellido, u.segundo_apellido, 
                   u.tipo_identificacion, u.numero_identificacion,
                   c.correo, c.telefono_principal, c.telefono_secundario
            FROM usuarios u
            JOIN credenciales c ON u.id_usuario = c.id_usuario
            WHERE u.id_usuario = :id_usuario
        """)
        result = session.execute(query, {"id_usuario": id_usuario}).fetchone()
        return result

def guardar_ticket(id_usuario, titulo, descripcion, estado, prioridad, id_categoria, id_asignado, archivo):

    """
    Guarda un nuevo ticket en la base de datos.

    Esta función inserta un ticket con la información proporcionada en la tabla de tickets.

    Args:
        id_usuario (int): El id del usuario que crea el ticket.
        titulo (str): El título del ticket.
        descripcion (str): La descripción detallada del problema o solicitud.
        estado (str): El estado inicial del ticket (por ejemplo, 'Pendiente').
        prioridad (str): La prioridad del ticket (por ejemplo, 'Alta').
        id_categoria (int): El id de la categoría del ticket.
        id_asignado (int): El id del usuario asignado al ticket.
        archivo (str or None): Ruta o nombre del archivo adjunto, si lo hay.

    Returns:
        bool: True si el ticket fue guardado correctamente, False en caso de error.
    """

    try:
        with engine.connect() as conexion:
            if archivo is None:
                archivo = None

            # Obtener la fecha de creación dentro de la función
            fecha_creacion = datetime.datetime.now()

            query = text("""INSERT INTO tickets (
                                id_usuario, titulo, descripcion, fecha_creacion, 
                                estado, prioridad, id_categoria, id_asignado, archivo
                            )
                            VALUES (
                                :id_usuario, :titulo, :descripcion, :fecha_creacion, 
                                :estado, :prioridad, :id_categoria, :id_asignado, :archivo
                            )""")
            
            parametros = {
                "id_usuario": id_usuario,
                "titulo": titulo,
                "descripcion": descripcion,
                "fecha_creacion": fecha_creacion, 
                "estado": estado,
                "prioridad": prioridad,
                "id_categoria": id_categoria,
                "id_asignado": id_asignado,
                "archivo": archivo
            }
            
            # Ejecutamos la consulta
            conexion.execute(query, parametros)
            conexion.commit()

            return True
    except Exception as e:
        print(f"Error al guardar el ticket: {e}")
        return False

def obtener_tickets(id_usuario):

    """
    Obtiene todos los tickets asociados a un usuario.

    Esta función consulta la base de datos para obtener todos los tickets relacionados 
    con un usuario específico.

    Args:
        id_usuario (int): El id del usuario cuyo tickets se desean obtener.

    Returns:
        list: Una lista de tuplas, cada una representando un ticket (id_ticket, título, descripción, etc.).
    """

    with Session(engine) as session:
        query = text("""
            SELECT t.id_ticket, t.titulo, t.descripcion, t.fecha_creacion, 
                   t.estado, t.prioridad, t.id_categoria, t.id_asignado, t.archivo
            FROM tickets t
            WHERE t.id_usuario = :id_usuario
        """)
        result = session.execute(query, {"id_usuario": id_usuario}).fetchall()
        return result

def actualizar_estado_ticket(id_ticket, nuevo_estado):

    """
    Actualiza el estado de un ticket.

    Esta función modifica el estado de un ticket específico en la base de datos. 
    Esto se utiliza para cambiar el estado de un ticket (por ejemplo, de 'Pendiente' a 'En proceso').

    Args:
        id_ticket (int): El id del ticket cuyo estado se desea actualizar.
        nuevo_estado (str): El nuevo estado del ticket.

    Returns:
        bool: True si el estado fue actualizado correctamente, False en caso de error.
    """

    try:
        with engine.connect() as conexion:
            query = text("""
                UPDATE tickets
                SET estado = :nuevo_estado
                WHERE id_ticket = :id_ticket
            """)
            conexion.execute(query, {"id_ticket": id_ticket, "nuevo_estado": nuevo_estado})
            conexion.commit()
            return True
    except Exception as e:
        print(f"Error al actualizar el estado del ticket: {e}")
        return False

def obtener_tickets_pendientes():

    """
    Obtiene todos los tickets pendientes o en proceso.

    Esta función consulta la base de datos para obtener los tickets que tienen un estado 
    de 'Pendiente' o 'En proceso'. Es útil para los administradores o personal de soporte 
    que gestionan los tickets activos.

    Returns:
        list: Una lista de tuplas con la información de los tickets pendientes (id_ticket, título, descripción, etc.).
    """

    try:
        with engine.connect() as conexion:
            query = text("""
                SELECT t.id_ticket, t.titulo, t.descripcion, t.estado, t.prioridad, u.nombre, u.apellido
                FROM tickets t
                JOIN usuarios u ON t.id_usuario = u.id_usuario
                WHERE t.estado IN ('Pendiente', 'En proceso')
            """)
            resultado = conexion.execute(query)
            tickets = resultado.fetchall()
            return tickets
    except Exception as e:
        print(f"Error al obtener los tickets pendientes: {e}")
        return []


def actualizar_estado_ticket(id_ticket, nuevo_estado, nueva_prioridad):

    """
    Actualiza el estado y la prioridad de un ticket.

    Esta función permite modificar tanto el estado como la prioridad de un ticket en la base de datos.

    Args:
        id_ticket (int): El id del ticket cuyo estado y prioridad se desean actualizar.
        nuevo_estado (str): El nuevo estado del ticket.
        nueva_prioridad (str): La nueva prioridad del ticket.

    Returns:
        bool: True si el ticket fue actualizado correctamente, False en caso de error.
    """

    try:
        with engine.connect() as conexion:
            query = text("""
                UPDATE tickets
                SET estado = :nuevo_estado, prioridad = :nueva_prioridad
                WHERE id_ticket = :id_ticket
            """)
            parametros = {
                "id_ticket": id_ticket,
                "nuevo_estado": nuevo_estado,
                "nueva_prioridad": nueva_prioridad
            }
            conexion.execute(query, parametros)
            conexion.commit()
            return True
    except Exception as e:
        print(f"Error al actualizar el ticket: {e}")
        return False

def obtener_respuestas_usuario(id_usuario):

    """
    Obtiene todas las respuestas asociadas a los tickets de un usuario.

    Esta función consulta la base de datos para obtener las respuestas de un usuario a sus tickets. 
    Se ordenan las respuestas por la fecha de creación de forma descendente.

    Args:
        id_usuario (int): El id del usuario cuyas respuestas se desean obtener.

    Returns:
        list: Una lista de tuplas con la información de las respuestas (id_respuesta, id_ticket, mensaje, fecha_respuesta).
    """

    with Session(engine) as session:
        query = text("""
            SELECT r.id_respuesta, r.id_ticket, r.mensaje, r.fecha_respuesta
            FROM respuestas_tickets r
            JOIN tickets t ON r.id_ticket = t.id_ticket
            WHERE t.id_usuario = :id_usuario
            ORDER BY r.fecha_respuesta DESC
        """)
        resultados = session.execute(query, {"id_usuario": id_usuario}).fetchall()
        return resultados

def guardar_respuesta_ticket(id_ticket, id_usuario, mensaje):

    """
    Guarda una nueva respuesta a un ticket.

    Esta función permite guardar una respuesta a un ticket en la base de datos. La respuesta se asocia 
    con un ticket y un usuario específicos.

    Args:
        id_ticket (int): El id del ticket al que se le responderá.
        id_usuario (int): El id del usuario que está respondiendo.
        mensaje (str): El contenido de la respuesta.

    Returns:
        bool: True si la respuesta fue guardada correctamente, False en caso de error.
    """
    
    try:
        with engine.connect() as conexion:
            fecha_respuesta = datetime.datetime.now()

            query = text("""
                INSERT INTO respuestas_tickets (id_ticket, id_usuario, mensaje, fecha_respuesta)
                VALUES (:id_ticket, :id_usuario, :mensaje, :fecha_respuesta)
            """)
            parametros = {
                "id_ticket": id_ticket,
                "id_usuario": id_usuario,
                "mensaje": mensaje,
                "fecha_respuesta": fecha_respuesta
            }
            conexion.execute(query, parametros)
            conexion.commit()
            return True
    except Exception as e:
        print(f"Error al guardar la respuesta del ticket: {e}")
        return False