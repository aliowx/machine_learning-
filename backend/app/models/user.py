from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base_class import Base


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    full_name: Mapped[str | None] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool | None] = mapped_column(Boolean(), default=True)
    is_superuser: Mapped[bool | None] = mapped_column(Boolean(), default=False)
