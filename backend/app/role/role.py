from enum import auto
from .enums import StrEnum




class UserRoles(StrEnum):
    ADMINISTRATOR = auto()
    APPS = auto()