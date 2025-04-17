from pydantic import BaseModel, ConfigDict, EmailStr

from typing import Optional


class UserBase(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None
    is_superuser: bool = False
    full_name: str | None = None
    