from enum import Enum 




class StrEnum(str, Enum):
    def __init__(self)-> None:...
    
    
    def __str__(self)-> str:
        return str(self.value)
    
    
    
    @classmethod
    def list_value(cls)-> list[str]:
        return [member.value for member in cls]
    
    
    @classmethod
    def has_value(cls, value: str)-> bool:
        return value in cls.list_value()