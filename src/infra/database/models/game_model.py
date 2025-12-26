from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.infra.database.config import Base

class GameModel(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)    
    console_id = Column(Integer, ForeignKey("consoles.id"), index=True, nullable=False)    
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)