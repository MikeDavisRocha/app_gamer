from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from src.domain.entities.game import Game

class IGameRepository(ABC):
    @abstractmethod
    async def create(self, game: Game) -> Game:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Game]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def list_with_filters(
        self, 
        skip: int, 
        limit: int, 
        name: Optional[str] = None, 
        console_id: Optional[int] = None
    ) -> Tuple[List[Game], int]:
        """
        Retorna uma tupla: (Lista de Jogos encontrados, Total de registros no banco para esse filtro)
        Precisamos do total para o frontend calcular quantas páginas existem.
        """
        pass