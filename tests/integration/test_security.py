import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.entities.user import User
from src.interface.api.dependencies import get_current_user
from src.interface.api.main import app


@pytest.mark.asyncio
async def test_regular_user_cannot_delete_console():
    """
    Testa se a API bloqueia corretamente um usuário comum (role='user')
    de tentar acessar uma rota de ADMIN (DELETE /consoles).
    """

    # 1. ARRANGE (Preparação com Mock)
    # Criamos um usuário falso que tem a role 'user' (comum)
    # Usamos o timezone-aware datetime para evitar warnings, se necessário, ou mock simples
    regular_user = User(
        id=999,
        username="Tester",
        email="test@test.com",
        password_hash="fake",
        role="user",
        created_at=None,
        updated_at=None,
    )

    # Ensinamos o FastAPI a usar nosso usuário falso em vez de checar token/banco
    app.dependency_overrides[get_current_user] = lambda: regular_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 2. ACT (Ação)
        # Tentamos deletar um console. Não precisamos de Header de Auth,
        # pois o override já injeta o usuário autenticado.
        response = await client.delete("/api/v1/consoles/1")

        # 3. ASSERT (Verificação)
        # O status DEVE ser 403 Forbidden (Proibido)
        assert response.status_code == 403

        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "HTTP_ERROR"

    # Limpeza: Removemos o override para não afetar outros testes
    app.dependency_overrides = {}
