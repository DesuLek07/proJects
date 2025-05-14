from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
import datetime

engine = create_engine('mysql+pymysql://root:desulek@localhost:3306/db_mesa_de_ayuda')

def verificar(nombre_usuario, contraseña):
    """
    Verifica las credenciales del usuario mediante procedimiento almacenado.
    """
    with engine.connect() as conexion:
        result = conexion.execute(text("CALL sp_verificar_usuario(:nombre_usuario, :contraseña)"),
                                  {"nombre_usuario": nombre_usuario, "contraseña": contraseña}).fetchone()
        if result:
            return result[0], result[1]
        return None, None

def registrar(nombre, segundo_nombre, apellido, segundo_apellido, tipo_id, numero_identificacion,
              fecha_registro, correo, contraseña_hash, telefono_principal,
              telefono_secundario, fecha_actualizacion, nombre_usuario):
    """
    Registra un nuevo usuario usando un procedimiento almacenado.
    """
    try:
        with engine.begin() as conexion:
            conexion.execute(text("""
                CALL sp_registrar_usuario(
                    :nombre, :segundo_nombre, :apellido, :segundo_apellido, :tipo_id,
                    :numero_identificacion, :fecha_registro, :correo, :contraseña_hash,
                    :telefono_principal, :telefono_secundario, :fecha_actualizacion, :nombre_usuario
                )
            """), {
                "nombre": nombre,
                "segundo_nombre": segundo_nombre,
                "apellido": apellido,
                "segundo_apellido": segundo_apellido,
                "tipo_id": tipo_id,
                "numero_identificacion": numero_identificacion,
                "fecha_registro": fecha_registro,
                "correo": correo,
                "contraseña_hash": contraseña_hash,
                "telefono_principal": telefono_principal,
                "telefono_secundario": telefono_secundario,
                "fecha_actualizacion": fecha_actualizacion,
                "nombre_usuario": nombre_usuario
            })
            return True
    except Exception as e:
        print("Error al registrar:", e)
        return False

def obtener_datos_usuario(id_usuario):
    """
    Obtiene los datos personales del usuario por procedimiento almacenado.
    """
    with Session(engine) as session:
        result = session.execute(text("CALL sp_obtener_datos_usuario(:id_usuario)"),
                                 {"id_usuario": id_usuario}).fetchone()
        return result

def guardar_ticket(id_usuario, titulo, descripcion, estado, prioridad, id_categoria, id_asignado, archivo):
    """
    Guarda un nuevo ticket mediante procedimiento almacenado.
    """
    try:
        with engine.begin() as conexion:
            conexion.execute(text("""
                CALL sp_guardar_ticket(
                    :id_usuario, :titulo, :descripcion, :estado, :prioridad, 
                    :id_categoria, :id_asignado, :archivo
                )
            """), {
                "id_usuario": id_usuario,
                "titulo": titulo,
                "descripcion": descripcion,
                "estado": estado,
                "prioridad": prioridad,
                "id_categoria": id_categoria,
                "id_asignado": id_asignado,
                "archivo": archivo
            })
            return True
    except Exception as e:
        print("Error al guardar el ticket:", e)
        return False

def obtener_tickets(id_usuario):
    """
    Obtiene todos los tickets de un usuario por procedimiento almacenado.
    """
    with Session(engine) as session:
        result = session.execute(text("CALL sp_obtener_tickets(:id_usuario)"),
                                 {"id_usuario": id_usuario}).fetchall()
        return result

def actualizar_estado_ticket(id_ticket, nuevo_estado, nueva_prioridad):
    """
    Actualiza estado y prioridad del ticket por procedimiento almacenado.
    """
    try:
        with engine.begin() as conexion:
            conexion.execute(text("""
                CALL sp_actualizar_ticket(:id_ticket, :nuevo_estado, :nueva_prioridad)
            """), {
                "id_ticket": id_ticket,
                "nuevo_estado": nuevo_estado,
                "nueva_prioridad": nueva_prioridad
            })
            return True
    except Exception as e:
        print("Error al actualizar el ticket:", e)
        return False

def obtener_tickets_pendientes():
    """
    Obtiene tickets pendientes o en proceso por procedimiento almacenado.
    """
    try:
        with engine.connect() as conexion:
            result = conexion.execute(text("CALL sp_obtener_tickets_pendientes()")).fetchall()
            return result
    except Exception as e:
        print("Error al obtener los tickets pendientes:", e)
        return []

def obtener_respuestas_usuario(id_usuario):
    """
    Obtiene respuestas de tickets del usuario por procedimiento almacenado.
    """
    with Session(engine) as session:
        resultados = session.execute(text("CALL sp_obtener_respuestas_usuario(:id_usuario)"),
                                     {"id_usuario": id_usuario}).fetchall()
        return resultados

def guardar_respuesta_ticket(id_ticket, id_usuario, mensaje):
    """
    Guarda respuesta a un ticket mediante procedimiento almacenado.
    """
    try:
        with engine.begin() as conexion:
            conexion.execute(text("""
                CALL sp_guardar_respuesta(:id_ticket, :id_usuario, :mensaje)
            """), {
                "id_ticket": id_ticket,
                "id_usuario": id_usuario,
                "mensaje": mensaje
            })
            return True
    except Exception as e:
        print("Error al guardar la respuesta del ticket:", e)
        return False
    
def obtener_historial_tickets_usuario(id_usuario):
    """
    Obtiene el historial completo de tickets de un usuario específico.

    Args:
        id_usuario (int): ID del usuario.

    Returns:
        list: Lista de tuplas con los datos de los tickets.
    """
    with Session(engine) as session:
        resultados = session.execute(
            text("CALL sp_historial_tickets_usuario(:id_usuario)"),
            {"id_usuario": id_usuario}
        ).fetchall()
        return resultados

def obtener_usuarios_registrados():
    """
    Llama al procedimiento almacenado `sp_obtener_usuarios` y retorna la lista de usuarios.

    Returns:
        list: Lista de tuplas con los usuarios, o una lista vacía si no hay resultados.
    """
    try:
        with Session(engine) as session:
            resultados = session.execute(text("CALL sp_obtener_usuarios()")).fetchall()
            return resultados
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    
def guardar_soporte(id_usuario, descripcion_problema, tipo_afectacion, entidad_atendio, medio_respuesta, info_medio_respuesta):
    """
    Guarda una solicitud de soporte mediante procedimiento almacenado.

    Args:
        id_usuario (int): ID del usuario que envía el soporte.
        descripcion_problema (str): Descripción del problema.
        tipo_afectacion (str): Tipo de problema seleccionado.
        entidad_atendio (str): Nombre de quien atendió.
        medio_respuesta (str): Medio elegido (Correo, Telefono o Whatsapp).
        info_medio_respuesta (str): Dato del medio (email, número, etc.).

    Returns:
        bool: True si se guardó correctamente, False en caso de error.
    """
    try:
        with engine.begin() as conexion:
            conexion.execute(text("""
                CALL sp_guardar_soporte(
                    :id_usuario, :descripcion_problema, :tipo_afectacion,
                    :entidad_atendio, :medio_respuesta, :info_medio_respuesta
                )
            """), {
                "id_usuario": id_usuario,
                "descripcion_problema": descripcion_problema,
                "tipo_afectacion": tipo_afectacion,
                "entidad_atendio": entidad_atendio,
                "medio_respuesta": medio_respuesta,
                "info_medio_respuesta": info_medio_respuesta
            })
        return True
    except Exception as e:
        print(f"Error al guardar soporte: {e}")
        return False

def obtener_registros_soporte():
    """
    Llama al procedimiento almacenado `sp_obtener_registros_soporte` y retorna los registros de soporte
    incluyendo el nombre del usuario y su rol.

    Returns:
        list: Lista de tuplas con los registros de soporte. Cada tupla contiene:
              (id_soporte, id_usuario, nombre_usuario, rol, descripcion_problema,
               tipo_afectacion, entidad_atendio, medio_respuesta, info_medio_respuesta)
              Retorna una lista vacía si no hay resultados o hay un error.
    """
    try:
        with Session(engine) as session:
            resultados = session.execute(text("CALL sp_obtener_registros_soporte()")).fetchall()
            return resultados
    except Exception as e:
        print(f"Error al obtener registros de soporte: {e}")
        return []

def actualizar_estado_ticket2(ticket_id, estado_ticket):
    """
    Llama al procedimiento almacenado `sp_actualizar_estado_ticket` para actualizar el estado
    de un ticket.

    Args:
        ticket_id (int): ID del ticket cuya estado se actualizará.
        estado_ticket (int): Nuevo estado del ticket (0 para cerrado, 1 para activo).

    Returns:
        bool: Retorna True si la actualización fue exitosa, False si hubo un error.
    """
    try:
        with Session(engine) as session:
            session.execute(text("CALL sp_actualizar_estado_ticket(:ticket_id, :estado_ticket)"), 
                            {"ticket_id": ticket_id, "estado_ticket": estado_ticket})
            session.commit()  # Aseguramos que la transacción se guarde
            return True
    except Exception as e:
        print(f"Error al actualizar estado del ticket {ticket_id}: {e}")
        return False

def escalar_soporte_a_ticket(id_soporte: int, id_admin: int) -> bool:
    """
    Llama al procedimiento almacenado `sp_escalar_soporte_a_ticket` para convertir un registro de soporte en un ticket.

    Args:
        id_soporte (int): ID del soporte que se quiere escalar.
        id_admin (int): ID del administrador al que se asignará el ticket.

    Returns:
        bool: True si la operación fue exitosa, False en caso de error.
    """
    try:
        with Session(engine) as session:
            session.execute(text("CALL sp_escalar_soporte_a_ticket(:id_soporte, :id_admin)"),
                            {"id_soporte": id_soporte, "id_admin": id_admin})
            session.commit()
            return True
    except Exception as e:
        print(f"Error al escalar soporte a ticket: {e}")
        return False

def reenviar_ticket_a_admin(id_ticket: int, id_soporte: int) -> bool:
    """
    Llama al procedimiento almacenado `sp_reenviar_ticket_a_admin` para marcar un ticket como reenviado al administrador.

    Args:
        id_ticket (int): ID del ticket a reenviar.
        id_soporte (int): ID del soporte que realiza el reenvío.

    Returns:
        bool: True si la operación fue exitosa, False en caso de error.
    """
    try:
        with Session(engine) as session:
            session.execute(
                text("CALL sp_reenviar_ticket_a_admin(:id_ticket, :id_soporte)"),
                {"id_ticket": id_ticket, "id_soporte": id_soporte}
            )
            session.commit()
            return True
    except Exception as e:
        print(f"Error al reenviar ticket a admin: {e}")
        return False
    
def obtener_administradores() -> list:
    """
    Llama al procedimiento almacenado `sp_obtener_administradores` para obtener la lista de administradores.

    Returns:
        list: Lista de administradores, cada uno como una tupla (id_usuario, nombre, apellido).
    """
    try:
        with Session(engine) as session:
            result = session.execute(text("CALL sp_obtener_administradores()"))
            administradores = result.fetchall()  # Obtener los resultados como lista de tuplas
            return administradores
    except Exception as e:
        print(f"Error al obtener administradores: {e}")
        return []
    
def obtener_chat(remitente_id, receptor_id):
    """
    Llama al procedimiento almacenado obtener_chat para traer los mensajes entre dos usuarios.

    Args:
        remitente_id (int): ID del administrador o soporte que consulta.
        receptor_id (int): ID del otro participante del chat.

    Returns:
        list: Lista de tuplas con (remitente_id, mensaje, timestamp).
    """
    with engine.connect() as conn:
        resultado = conn.execute(text("CALL obtener_chat(:rem, :rec)"),
                                 {"rem": remitente_id, "rec": receptor_id})
        return resultado.fetchall()
    
def enviar_mensaje_chat(remitente_id, receptor_id, mensaje):
    """
    Inserta un nuevo mensaje en el chat entre dos usuarios mediante un procedimiento almacenado.

    Args:
        remitente_id (int): ID del remitente (admin o soporte).
        receptor_id (int): ID del destinatario.
        mensaje (str): Texto del mensaje.
    """
    with engine.connect() as conn:
        conn.execute(text("CALL enviar_mensaje_chat(:rem, :rec, :msg)"),
                     {"rem": remitente_id, "rec": receptor_id, "msg": mensaje})
        
def obtener_info_usuario(id_usuario):
    """
    Obtiene la información de un usuario específico mediante un procedimiento almacenado.

    Args:
        id_usuario (int): El ID del usuario cuya información se desea obtener.

    Returns:
        tuple: Una tupla con los datos del usuario o None si no se encuentra.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("CALL obtener_info_usuario(:id)"), {"id": id_usuario}).fetchone()

        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error al obtener información del usuario: {e}")
        return None

