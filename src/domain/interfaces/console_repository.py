from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.console import Console

class IConsoleRepository(ABC):
    @abstractmethod
    async def create(self, console: Console) -> Console:
        pass

    @abstractmethod
    async def list_all(self) -> List[Console]:
        """Lista apenas consoles não deletados"""
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Console]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Realiza o Soft Delete"""
        pass