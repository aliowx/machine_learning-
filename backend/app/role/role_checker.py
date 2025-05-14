from typing import Annotated
from fastapi import Depends
from app import exceptions as exc
from app.role.role import UserRoles
from app.api import deps
from app.models.user import User
from app.utils.message_codes import MessageCodes



class RoleChecker:
    def __init__(self, allowed_roles: list[UserRoles])-> UserRoles: self.allowed_roles = allowed_roles
    
    
    
    def __call__(self, *args, **kwds):
        pass
    
    
    