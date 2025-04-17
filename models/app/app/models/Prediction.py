from sqlalchemy import SQLColumnExpression
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    func
)

class Prediction(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE'),
        index=True
    )  
    model_version_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('ModelVersion.id'),
        nullable=False
    )
    prediction_result: Mapped[str] = mapped_column(
        String
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    