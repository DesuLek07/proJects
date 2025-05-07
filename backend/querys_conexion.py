from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
import datetime

engine = create_engine('mysql+pymysql://root:desulek@localhost:3306/db_mesa_de_ayuda')

def verificar(nombre_usuario, contraseña):
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
