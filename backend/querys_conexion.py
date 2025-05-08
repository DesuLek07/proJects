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
