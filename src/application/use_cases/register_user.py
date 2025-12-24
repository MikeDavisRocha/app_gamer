from src.domain.interfaces.user_repository import IUserRepository
from src.application.dtos.user_dto import UserCreateInput, UserOutput
from src.domain.entities.user import User, UserRole
from src.core.security import get_password_hash
from src.core.exceptions import UserAlreadyExistsError

class RegisterUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, input_data: UserCreateInput) -> UserOutput:
        # 1. Regra de Negócio: Email deve ser único
        existing_user = await self.repository.get_by_email(input_data.email)
        if existing_user:
            raise UserAlreadyExistsError("Email already registered")

        # 2. Segurança: Hash da senha
        hashed_password = get_password_hash(input_data.password)

        # 3. Criação da Entidade
        new_user = User(
            id=None, # O banco vai gerar
            username=input_data.username,
            email=input_data.email,
            password_hash=hashed_password,
            role=UserRole.USER # Todo registro público começa como User
        )

        # 4. Persistência
        saved_user = await self.repository.create(new_user)

        # 5. Retorno (Converte Entity -> DTO)
        return UserOutput(
            id=saved_user.id,
            username=saved_user.username,
            email=saved_user.email,
            role=saved_user.role
        )