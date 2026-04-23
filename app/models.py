from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Conexión a la base de datos
engine = create_engine('mysql+pymysql://root:2007@localhost/db_mesa_de_ayuda')

Base = declarative_base()   

class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    tipo_rol = Column(String(20), nullable=False, default='Usuario')

    # Relación con usuarios
    usuarios = relationship('Usuarios', back_populates='rol')

    def __str__(self):
        return self.tipo_rol


class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    primer_nombre = Column(String(50), nullable=False)
    segundo_nombre = Column(String(50), nullable=True)
    primer_apellido = Column(String(50), nullable=False)
    segundo_apellido = Column(String(50), nullable=False)
    tipo_documento = Column(String(15), nullable=False)
    numero_documento = Column(String(15), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    correo = Column(String(50), nullable=False, unique=True)
    contrasena = Column(String(50), nullable=False)
    rol_id = Column(Integer(), ForeignKey('roles.id'), nullable=False)
    creado_el = Column(DateTime(), default=datetime.now)

    # Relaciones
    rol = relationship('Roles', back_populates='usuarios')
    tickets = relationship('Tickets', back_populates='user')

    def __str__(self):
        return self.username


class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    titulo = Column(String(50), nullable=False)
    descripcion = Column(String(200), nullable=False)
    estado = Column(String(20), default='Abierto')
    prioridad = Column(String(20), nullable=False)
    categoria = Column(String(50), nullable=False)
    usuario_id = Column(Integer(), ForeignKey('usuarios.id'), nullable=True)
    fecha_creacion = Column(DateTime(), default=datetime.now, nullable=False)
    fecha_solucion = Column(DateTime(), nullable=True)

    # Relación con usuarios
    user = relationship('Usuarios', back_populates='tickets')

    respuestas = relationship('RespuestasTickets', back_populates='ticket', cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.titulo} - {self.estado}"

class RespuestasTickets(Base):
    __tablename__ = 'respuestas_tickets'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    ticket_id = Column(Integer(), ForeignKey('tickets.id'), nullable=False)
    usuario_id = Column(Integer(), ForeignKey('usuarios.id'), nullable=False)
    mensaje = Column(String(500), nullable=False)
    fecha_respuesta = Column(DateTime(), default=datetime.now, nullable=False)

    # Relaciones
    ticket = relationship('Tickets', back_populates='respuestas')
    usuario = relationship('Usuarios')

    def __str__(self):
        return f"Respuesta de {self.usuario.username} en Ticket #{self.ticket_id}"
    
class Mensajes(Base):
    __tablename__ = 'mensajes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    contenido = Column(String(1000), nullable=False)
    fecha_envio = Column(DateTime, default=datetime.now)
    estado = Column(String(20), default='Enviado')

    # Relaciones
    emisor = relationship('Usuarios', foreign_keys=[sender_id])
    receptor = relationship('Usuarios', foreign_keys=[receiver_id])

    def __str__(self):
        return f"{self.emisor.username} → {self.receptor.username}: {self.contenido[:30]}"



# Crear sesión
Session = sessionmaker(engine)
sesion = Session()

#if __name__ == '__main__':
#    Base.metadata.drop_all(engine) 
#    Base.metadata.create_all(engine) 