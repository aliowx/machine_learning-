from sqlalchemy import Integer, String, Text, Float
from sqlalchemy.orm import mapped_column, Mapped
from app.app.db.base_class import Base


class RequestLog(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[str | None] = mapped_column(String(50))
    method: Mapped[str | None] = mapped_column(String(10))
    service_name: Mapped[str | None] = mapped_column(Text)
    processing_time: Mapped[float | None] = mapped_column(Float)
    tracker_id: Mapped[str | None] = mapped_column(String(100))
    ip: Mapped[str | None] = mapped_column(String(50))
    request: Mapped[str | None] = mapped_column(Text)
    response: Mapped[str | None] = mapped_column(Text)
    trace: Mapped[str | None] = mapped_column(Text, default="")

    def __str__(self):
        return "%s: %s, %s" % (self.service_name, self.ip, self.created)
