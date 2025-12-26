from sqlalchemy import Column, Integer, String, DateTime
from src.infra.database.config import Base

class ConsoleModel(Base):
    __tablename__ = "consoles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    company = Column(String, index=True, nullable=False)    
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)