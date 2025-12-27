from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy import asc, desc, func, select
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
        game.updated_at = model.updated_at
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
        self, 
        skip: int, 
        limit: int, 
        name: Optional[str] = None, 
        console_id: Optional[int] = None,
        sort_by: str = "name",
        sort_order: str = "asc"
    ) -> Tuple[List[Game], int]:
        
        # 1. Base da Query: Apenas não deletados
        query = select(GameModel).where(GameModel.deleted_at.is_(None))

        # 2. Aplica Filtros Dinâmicos
        if name:
            query = query.where(GameModel.name.ilike(f"%{name}%"))

        if console_id:
            query = query.where(GameModel.console_id == console_id)

        # 3. Contar o total (Count)
        # Usamos select(func.count()) na query filtrada para saber o total de páginas
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        # 4. Aplica Ordenação Dinâmica
        field_map = {
            "name": GameModel.name,
            "created_at": GameModel.created_at
        }
        # Se o campo não existir no mapa, usa 'name' como padrão
        sort_column = field_map.get(sort_by, GameModel.name)
        
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # 5. Aplica Paginação e Executa
        query = query.offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        models = result.scalars().all()

        games = [
            Game(
                id=m.id, 
                name=m.name, 
                console_id=m.console_id, 
                created_at=m.created_at, 
                updated_at=m.updated_at
            )
            for m in models
        ]

        return games, total

    async def delete(self, id: int) -> bool:
        query = select(GameModel).where(GameModel.id == id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if not model:
            return False

        model.deleted_at = datetime.now(timezone.utc)
        
        await self.session.commit()
        return True