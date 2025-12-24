from pydantic import BaseModel, EmailStr, Field
from src.domain.entities.user import UserRole

# O que o front-end envia para cadastrar
class UserCreateInput(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

# O que devolvemos para o front-end (sem a senha!)
class UserOutput(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True # Permite converter da Entity/Model para o Pydantic