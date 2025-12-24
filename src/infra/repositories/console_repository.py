from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.interfaces.console_repository import IConsoleRepository
from src.domain.entities.console import Console
from src.infra.models.console import ConsoleModel

class ConsoleRepository(IConsoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, console: Console) -> Console:
        db_console = ConsoleModel(
            name=console.name,
            company=console.company
        )
        self.session.add(db_console)
        await self.session.commit()
        await self.session.refresh(db_console)
        
        console.id = db_console.id
        console.created_at = db_console.created_at
        return console

    async def list_all(self) -> List[Console]:
        # Filtra apenas os que NÃO foram deletados (deleted_at IS NULL)
        query = select(ConsoleModel).where(ConsoleModel.deleted_at.is_(None))
        result = await self.session.execute(query)
        models = result.scalars().all()
        
        return [
            Console(
                id=m.id, name=m.name, company=m.company, 
                created_at=m.created_at, updated_at=m.updated_at
            ) for m in models
        ]

    async def get_by_id(self, id: int) -> Optional[Console]:
        query = select(ConsoleModel).where(ConsoleModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()
        
        # Se não existe ou foi deletado (soft delete), retorna None
        if not model or model.deleted_at is not None:
            return None
            
        return Console(
            id=model.id, name=model.name, company=model.company,
            created_at=model.created_at, updated_at=model.updated_at
        )

    async def delete(self, id: int) -> bool:
        query = select(ConsoleModel).where(ConsoleModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()
        
        if not model:
            return False
            
        # Implementação do Soft Delete
        model.deleted_at = datetime.utcnow()
        await self.session.commit()
        return True