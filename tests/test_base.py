import unittest
import sys
import os

# Agregar carpeta app al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app


class BasicRoutesTestCase(unittest.TestCase):
    """Pruebas básicas de rutas sin base de datos."""

    def setUp(self):
        # Configurar test client
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_root_redirects_to_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('/login', response.location)

    def test_login_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Iniciar sesión', response.data.decode('utf-8'))

    def test_register_get(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registrar', response.data.decode('utf-8'))

    def test_forgot_password_get(self):
        response = self.client.get('/forgot_password')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Solicitar recuperación', response.data.decode('utf-8'))

    def test_dashboard_redirect_without_login(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

    def test_logout_redirects(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)


if __name__ == '__main__':
    unittest.main()
