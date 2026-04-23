import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app
from app.models import Base, Usuarios, Roles, Tickets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


class FullAppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )

        cls.Session = sessionmaker(bind=engine)
        cls.db_session = cls.Session()

        # reemplazar la sesión global
        app.sesion = cls.db_session

        app.config["TESTING"] = True
        cls.client = app.test_client()

        Base.metadata.create_all(engine)

        # Crear roles
        admin = Roles(tipo_rol="Administrador")
        user = Roles(tipo_rol="Usuario")
        soporte = Roles(tipo_rol="Soporte")
        cls.db_session.add_all([admin, user, soporte])
        cls.db_session.commit()

        # Usuario de prueba
        cls.test_user = Usuarios(
            tipo_documento="CC",
            numero_documento="12345678",
            primer_nombre="Miguel",
            segundo_nombre="",
            primer_apellido="Leon",
            segundo_apellido="Test",
            username="miguel_test",
            correo="miguel@test.com",
            contrasena="pass123",
            rol_id=user.id,
        )
        cls.db_session.add(cls.test_user)
        cls.db_session.commit()


    # ✅ TEST: duplicado en registro
    def test_register_duplicate_username(self):
        response = self.client.post("/register", data={
            "tipo_de_documento": "CC",
            "numberd": "87654321",
            "primer_nombre": "Juan",
            "primer_apellido": "Perez",
            "username": "miguel_test",
            "correo": "juan@test.com",
            "password": "abc123"
        }, follow_redirects=True)

        # ahora se valida que se muestre el mensaje flash
        response_text = response.data.decode().lower()
        self.assertTrue(
            ("usuario o correo ya existente" in response_text) or
            ("ese número de documento ya está registrado" in response_text)
        )

    # ✅ TEST: login correcto
    def test_login_success_redirect(self):
        response = self.client.post("/login", data={
            "username": "miguel_test",
            "password": "pass123"
        }, follow_redirects=False)

        # ahora se espera redirect a dashboard
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.location)


    # ✅ TEST: crear ticket
    def test_crear_ticket(self):
        with self.client.session_transaction() as sess:
            sess["user_id"] = self.test_user.id
            sess["rol"] = "Usuario"

        response = self.client.post("/crear_ticket", data={
            "titulo": "Ticket prueba",
            "descripcion": "Descripción prueba",
            "categoria": "Soporte",
            "prioridad": "Alta"
        }, follow_redirects=True)

        self.assertIn("ticket creado con éxito", response.data.decode().lower())

        ticket = app.sesion.query(Tickets).filter_by(titulo="Ticket prueba").first()
        self.assertIsNotNone(ticket)


    # ✅ TEST: dashboard muestra el nombre correcto
    def test_dashboard_with_session(self):
        with self.client.session_transaction() as sess:
            sess["user_id"] = self.test_user.id
            sess["nombre"] = "Miguel"  # nombre usado por tu dashboard

        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn("miguel", response.data.decode().lower())


if __name__ == "__main__":
    unittest.main()
