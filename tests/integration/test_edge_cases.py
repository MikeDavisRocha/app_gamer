from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.entities.user import User
from src.interface.api.main import app

try:
    from src.interface.api.v1.endpoints.auth import get_current_user
except ImportError:
    from src.interface.api.dependencies import get_current_user


@pytest.mark.asyncio
async def test_get_non_existent_console_returns_404():
    """
    Teste de Edge Case: Tentar buscar um recurso que não existe.
    Requisito: Testes de erro e edge cases
    """
    # 1. ARRANGE
    mock_user = User(
        id=1, username="test", email="test@test.com", password_hash="x", role="user", created_at=None, updated_at=None
    )

    # Override do usuário
    app.dependency_overrides[get_current_user] = lambda: mock_user

    try:
        # Mock do repositório para retornar None (console não encontrado)
        with patch(
            "src.infra.repositories.console_repository.ConsoleRepository.get_by_id",
            new_callable=AsyncMock,
            return_value=None,
        ):
            # 2. ACT & ASSERT
            transport = ASGITransport(app=app)

            async with AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get("/api/v1/consoles/999999")

                # Verifica o status code
                assert response.status_code == 404

                # Verifica a estrutura da resposta
                data = response.json()
                assert data["success"] is False
                assert data["error"]["code"] == "NOT_FOUND"
                assert "999999" in str(data["error"]["message"])
    finally:
        # Limpeza
        app.dependency_overrides.clear()
