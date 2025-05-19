from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    JSON
)
from datetime import datetime, UTC

class ProcessedFile(Base):
    
    task_id: Mapped[str]= mapped_column(String, primary_key=True)
    result: Mapped[JSON] = mapped_column(JSON)  # JSON result
    
    status: Mapped[str] = mapped_column(String, default="PENDING")  # PENDING, SUCCESS, FAILED
    error_message: Mapped[str] = mapped_column(String, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)