from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.interfaces.user_repository import IUserRepository
from src.domain.entities.user import User
from src.infra.models.user import UserModel

class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        user_model = result.scalars().first()
        
        if user_model:
            # Converte Model (Infra) -> Entity (Domain)
            return User(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                password_hash=user_model.password_hash,
                role=user_model.role
            )
        return None

    async def create(self, user: User) -> User:
        # Converte Entity (Domain) -> Model (Infra)
        user_model = UserModel(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role
        )
        
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        
        # Devolve a entidade com o ID gerado
        user.id = user_model.id
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        user_model = result.scalars().first()

        if user_model:
            return User(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                password_hash=user_model.password_hash,
                role=user_model.role
            )
        return None