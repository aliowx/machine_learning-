from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.app.crud.base import CRUDBase
from app.app.models.request_log import RequestLog
from app.app.schemas.request_log import RequestLogCreate, RequestLogUpdate



class CRUDRequestLog(CRUDBase[RequestLog, RequestLogCreate, RequestLogUpdate]):
    
    async def get_by_tracker_id(
        self,
        db: AsyncSession,
        tracker_id: int | str
    )-> RequestLog | None:
        query = select(self.model).where(
            and_(
                self.model.tracker_id == tracker_id,
                self.model.is_deleted.is_(None),
            ),
        )
        response = await db.execute(query)
        return response.scalar_one_or_none()
    
    
request_log = CRUDRequestLog(RequestLog)
