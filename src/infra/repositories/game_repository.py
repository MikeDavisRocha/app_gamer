from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.game import Game
from src.domain.interfaces.game_repository import IGameRepository
from src.infra.models.game import GameModel


class GameRepository(IGameRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, game: Game) -> Game:
        model = GameModel(name=game.name, console_id=game.console_id)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        game.id = model.id
        game.created_at = model.created_at
        return game

    async def get_by_id(self, id: int) -> Optional[Game]:
        query = select(GameModel).where(GameModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if not model or model.deleted_at is not None:
            return None

        return Game(
            id=model.id,
            name=model.name,
            console_id=model.console_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def list_with_filters(
        self, skip: int, limit: int, name: Optional[str] = None, console_id: Optional[int] = None
    ) -> Tuple[List[Game], int]:
        # 1. Base da Query: Apenas não deletados
        query = select(GameModel).where(GameModel.deleted_at.is_(None))

        # 2. Aplica Filtros Dinâmicos
        if name:
            # ILIKE faz busca case-insensitive (ex: "mario" acha "Super Mario")
            query = query.where(GameModel.name.ilike(f"%{name}%"))

        if console_id:
            query = query.where(GameModel.console_id == console_id)

        # 3. Contar o total de resultados (sem paginação) para o frontend saber
        # Precisamos fazer uma subquery ou count separado para performance correta
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        # 4. Aplicar Paginação e Ordenação
        query = query.offset(skip).limit(limit).order_by(GameModel.name.asc())

        # 5. Executar
        result = await self.session.execute(query)
        models = result.scalars().all()

        games = [
            Game(id=m.id, name=m.name, console_id=m.console_id, created_at=m.created_at, updated_at=m.updated_at)
            for m in models
        ]

        return games, total

    async def delete(self, id: int) -> bool:
        query = select(GameModel).where(GameModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if not model:
            return False

        model.deleted_at = datetime.utcnow()
        await self.session.commit()
        return True
