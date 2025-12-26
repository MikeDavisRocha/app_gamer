import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from src.interface.api.main import app


# Configura o Pytest para aceitar funções async
@pytest.mark.asyncio
async def test_register_login_and_access_protected_route():
    # Setup: Criar um cliente de teste que "finge" ser um navegador
    # Usamos ASGITransport para conectar direto na aplicação FastAPI sem precisar subir o servidor
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # ----------------------------------------------------------------
        # 1. REGISTRO (Sign Up)
        # ----------------------------------------------------------------
        # Geramos um email único para não falhar se rodar o teste 2 vezes
        unique_email = f"user_{uuid.uuid4()}@teste.com"
        user_payload = {"username": "Test User", "email": unique_email, "password": "password123"}

        response_register = await client.post("/auth/register", json=user_payload)

        # Validações
        assert response_register.status_code == 201
        data_register = response_register.json()
        assert data_register["success"] is True
        assert data_register["data"]["email"] == unique_email
        print(f"\n[OK] Usuário registrado: {unique_email}")

        # ----------------------------------------------------------------
        # 2. LOGIN (Sign In)
        # ----------------------------------------------------------------
        login_payload = {"email": unique_email, "password": "password123"}

        response_login = await client.post("/auth/login", json=login_payload)

        # Validações
        assert response_login.status_code == 200
        data_login = response_login.json()
        assert "access_token" in data_login["data"]

        token = data_login["data"]["access_token"]
        print("[OK] Login realizado. Token capturado.")

        # ----------------------------------------------------------------
        # 3. ROTA PROTEGIDA (/auth/me)
        # ----------------------------------------------------------------
        headers = {"Authorization": f"Bearer {token}"}

        response_me = await client.get("/auth/me", headers=headers)

        # Validações
        assert response_me.status_code == 200
        data_me = response_me.json()
        assert data_me["data"]["email"] == unique_email
        print("[OK] Acesso à rota protegida confirmado.")
