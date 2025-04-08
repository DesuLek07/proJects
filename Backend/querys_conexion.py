from sqlalchemy import text, create_engine

engine = create_engine('mysql+pymysql://root:desulek@localhost:3306/db_mesa_de_ayuda')

def verificar(nombre_usuario, contraseña):
    with engine.connect() as conexion:
        query = text('SELECT * FROM credenciales WHERE nombre_usuario = :nombre_usuario AND contraseña_hash = :contraseña')
        result = conexion.execute(query, {'nombre_usuario': nombre_usuario, 'contraseña': contraseña}).fetchone()
        return result is not None
    
def registrar(nombre, segundo_nombre, apellido, segundo_apellido, tipo_id, numero_identificacion, fecha_registro, correo, contraseña_hash, telefono_principal, telefono_secundario, fecha_actualizacion, nombre_usuario):
    try:
        with engine.connect() as conexion:
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
