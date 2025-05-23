from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base
from sqlalchemy import (
    DateTime,
    Column,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
    JSON
)
from .user import User


class ChatHistory(Base):
    id: Mapped[int] =  mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    
    user_message: Mapped[str] = mapped_column(String)
    bot_response: Mapped[str] = mapped_column(String)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now())