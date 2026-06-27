import unittest
from mockito import mock, when, unstub, verify
from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.services.auth_service import repo as auth_repo
from app.schemas.schemas import LoginRequest
from app.models.models import Usuario
from app.security import hash_password

class TestAuthServiceMockito(unittest.TestCase):
    def tearDown(self):
        unstub()  # Clean up mocks after each test

    def test_login_success(self):
        # Mock database session
        mock_db = mock()
        
        # Create a mock user
        mock_user = Usuario(
            id=42,
            username="test_mockito",
            email="mockito@test.com",
            password_hash=hash_password("Password123"),
            activo=True
        )
        
        # Stub the repo call using mockito's when()
        when(auth_repo).obtener_por_username_o_email(mock_db, "test_mockito").thenReturn(mock_user)
        
        # Execute service login
        service = AuthService()
        payload = LoginRequest(username_or_email="test_mockito", password="Password123")
        result = service.login(mock_db, payload)
        
        # Validate output
        self.assertIsNotNone(result)
        self.assertEqual(result["token_type"], "bearer")
        self.assertIn("access_token", result)
        self.assertIn("refresh_token", result)
        
        # Verify the stubbed method was indeed called
        verify(auth_repo).obtener_por_username_o_email(mock_db, "test_mockito")

    def test_login_invalid_user(self):
        mock_db = mock()
        
        # Stub the repo to return None (user not found)
        when(auth_repo).obtener_por_username_o_email(mock_db, "unknown").thenReturn(None)
        
        service = AuthService()
        payload = LoginRequest(username_or_email="unknown", password="Password123")
        
        # Check that it raises a 401 HTTPException
        with self.assertRaises(HTTPException) as context:
            service.login(mock_db, payload)
            
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Credenciales inválidas")
