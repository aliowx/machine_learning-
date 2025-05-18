from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
    JSON
)



class MLModel(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    model_name : Mapped[str] = mapped_column(String)
    
    framework: Mapped[str] = mapped_column(String, nullable=False)
    
    inputs: Mapped[JSON] = mapped_column(JSON)
    
    outputs: Mapped[JSON] = mapped_column(JSON)
    
    preprocessing: Mapped[JSON] = mapped_column(JSON)
    version_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    
    model_file_path: Mapped[str] = mapped_column(String, nullable=False)
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    