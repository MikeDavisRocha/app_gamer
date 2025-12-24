from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.infra.database.config import Base

class ConsoleModel(Base):
    __tablename__ = "consoles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    company = Column(String, index=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True) # Null = Ativo