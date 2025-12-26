from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.dtos.console_dto import ConsoleCreateInput

# Imports do nosso projeto
from src.application.use_cases.console_use_cases import CreateConsoleUseCase
from src.domain.entities.console import Console
from src.domain.interfaces.console_repository import IConsoleRepository


@pytest.mark.asyncio
async def test_should_create_console_successfully():
    """
    Testa se o UseCase chama o repositório corretamente e retorna os dados.
    NÃO usa banco de dados real.
    """

    # 1. ARRANGE (Preparação)
    # Criamos um "Dublê" do repositório
    mock_repo = MagicMock(spec=IConsoleRepository)

    # Dados de entrada
    input_dto = ConsoleCreateInput(name="PlayStation 5", company="Sony")

    # O que o "banco de mentira" deve devolver quando chamarem o .create()
    fake_saved_console = Console(
        id=10, name="PlayStation 5", company="Sony", created_at=datetime.now(), updated_at=datetime.now()
    )

    # Ensinamos o Mock a retornar esse objeto de forma assíncrona
    mock_repo.create = AsyncMock(return_value=fake_saved_console)

    # Instanciamos o UseCase passando o Mock em vez do Repo real
    use_case = CreateConsoleUseCase(mock_repo)

    # 2. ACT (Ação)
    result = await use_case.execute(input_dto)

    # 3. ASSERT (Verificação)
    assert result.id == 10
    assert result.name == "PlayStation 5"
    assert result.company == "Sony"

    # A prova final: Verificamos se o método .create() do repo foi chamado exatamente 1 vez
    mock_repo.create.assert_called_once()
