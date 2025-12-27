import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from src.interface.api.main import app

@pytest.mark.asyncio
async def test_register_login_and_access_protected_route():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        # 1. REGISTRO (Sign Up)
        random_id = str(uuid.uuid4())
        unique_email = f"user_{random_id}@teste.com"
        
        user_payload = {
            "username": f"User {random_id}",
            "email": unique_email,
            "password": "password123"
        }

        response_register = await client.post("/auth/register", json=user_payload)
        assert response_register.status_code == 201, f"Erro no registro: {response_register.text}"
        data_register = response_register.json()
        assert data_register["success"] is True

        # 2. LOGIN (Sign In)
        login_payload = {
            "email": unique_email,
            "password": "password123"
        }

        response_login = await client.post(
            "/auth/login",
            json=login_payload
        )
        
        assert response_login.status_code == 200, f"Erro no login: {response_login.text}"
        token_data = response_login.json()
        
        # CORREÇÃO: acesse o token dentro de "data"
        access_token = token_data["data"]["access_token"]
        assert access_token is not None

        # 3. ACESSAR ROTA PROTEGIDA
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response_protected = await client.get("/consoles/", headers=headers)
        assert response_protected.status_code == 200