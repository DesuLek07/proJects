"""
===========================================
Dongo HelpDesk - Módulo de Chat en Tiempo Real
===========================================

Este módulo implementa el chat en tiempo real para el sistema **Dongo HelpDesk**,
utilizando Flask y Flask-SocketIO. Permite la comunicación entre usuarios y administradores
dentro de salas dinámicas.

This module implements the real-time chat system for **Dongo HelpDesk**,
using Flask and Flask-SocketIO. It enables communication between users and administrators
inside dynamic chat rooms.

Módulo desarrollado por:
------------------------
- Miguel Ángel León León

Fecha: Abril 2026
"""

from flask import Flask, render_template, session, redirect, url_for, request
from flask_socketio import SocketIO, send, emit, join_room
from datetime import datetime

# ======================================
#  Configuración inicial / Initial setup
# ======================================

#: Instancia principal de la aplicación Flask.
#: Main Flask application instance.
app = Flask(__name__)

#: Clave secreta para sesiones y seguridad de Flask.
#: Secret key for Flask sessions and security.
app.config['SECRET_KEY'] = 'clave_secreta_chat'

#: Objeto principal de SocketIO que gestiona la comunicación en tiempo real.
#: Main SocketIO object that handles real-time communication.
socketio = SocketIO(app, cors_allowed_origins="*")  # Permite comunicación en local y red / Allows LAN communication

#: Diccionario para rastrear usuarios y las salas a las que pertenecen.
#: Dictionary to track users and the rooms they belong to.
rooms = {}


# ======================================
#  Ruta principal / Main route
# ======================================

@app.route('/')
def index():
    """
    Página principal del chat.  
    Main chat page.

    Returns
    -------
    flask.Response
        Renderiza la plantilla ``chat.html`` con el nombre de usuario y rol si la sesión está activa.  
        Renders the ``chat.html`` template with the username and role if the session is active.

    Redirects
    ---------
    Si no hay sesión activa, redirige a la vista de ``login``.  
    If no session is active, redirects to the ``login`` view.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    username = session.get('usuario')
    rol = session.get('rol', 'Usuario')

    return render_template('chat.html', username=username, rol=rol)


# ======================================
#  EVENTOS SOCKET.IO
# ======================================

@socketio.on('join')
def handle_join(data):
    """
    Maneja el evento cuando un usuario se une a una sala.  
    Handles the event when a user joins a chat room.

    Parameters
    ----------
    data : dict
        Diccionario con las claves ``username`` (nombre de usuario) y ``room`` (sala a la que se une).  
        Dictionary with keys ``username`` (user name) and ``room`` (room joined).

    Emits
    -----
    message : dict
        Envía un mensaje a todos los usuarios en la sala notificando que el usuario se ha unido.  
        Sends a message to all users in the room notifying that the user has joined.
    """
    username = data['username']
    room = data['room']

    join_room(room)
    rooms[username] = room

    emit('message', {'msg': f"🟢 {username} se ha unido al chat."}, room=room)
    print(f"{username} se unió a la sala {room}")


@socketio.on('message')
def handle_message(data):
    """
    Maneja el envío de mensajes dentro de una sala.  
    Handles message sending inside a chat room.

    Parameters
    ----------
    data : dict
        Contiene ``username``, ``msg`` y ``room``.  
        Contains ``username``, ``msg``, and ``room``.

    Emits
    -----
    message : dict
        Envía el mensaje formateado con hora y usuario a todos los clientes en la sala.  
        Sends the formatted message with time and user to all clients in the room.
    """
    username = data['username']
    msg = data['msg']
    room = data['room']

    hora = datetime.now().strftime("%H:%M:%S")
    mensaje = f"[{hora}] {username}: {msg}"

    send({'msg': mensaje}, room=room)
    print(f"💬 {mensaje} (en sala {room})")


@socketio.on('disconnect')
def handle_disconnect():
    """
    Maneja la desconexión de un usuario.  
    Handles user disconnection.

    Emits
    -----
    message : dict
        Envía un mensaje notificando que el usuario salió del chat.  
        Sends a message notifying that the user left the chat.
    """
    for user, room in list(rooms.items()):
        emit('message', {'msg': f"🔴 {user} salió del chat."}, room=room)
        del rooms[user]
        print(f"{user} se desconectó del chat.")
        break


# ======================================
#  EJECUCIÓN / APP RUN
# ======================================

if __name__ == '__main__':
    print("💬 Servidor de chat en tiempo real activo en http://localhost:5861/")
    socketio.run(app, port=5861, debug=True, host='0.0.0.0')
