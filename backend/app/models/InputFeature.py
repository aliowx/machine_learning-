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

class InputFeature(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    prediction_id: Mapped[int] = mapped_column(
        Integer,
        index=True
    )
    
    feature_name: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    
    feature_value: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
