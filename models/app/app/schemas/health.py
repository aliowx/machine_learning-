from pydantic import BaseModel

class Status(BaseModel):
    ok: bool = None
    msg: str = None
    time: float = None
    
    
class Services(BaseModel):
    redis: Status = Status()
    postgres: Status = Status()
    

class HealthCheck(BaseModel):
    ok: bool = True
    package_name: str = "prediction"
    app_version: str | None = None
    commit_id: str | None = None
    uptime: float | None = None
    human_readable_uptime: str | None = None
    services: Services = Services()
