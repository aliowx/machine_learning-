from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from app.app.db.base_class import Base
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    text,
    ARRAY,
    Boolean
)
class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
   
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
      
    Username: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=True)
    
    role: Mapped[str] = mapped_column(String, nullable=True, index=True)  
    