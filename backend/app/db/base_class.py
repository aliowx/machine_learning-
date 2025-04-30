from datetime import datetime
from typing import Any

from persiantools.jdatetime import JalaliDate
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime


class Base(DeclarativeBase):
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    is_deleted = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )
    created = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    modified = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        index=True,
        onupdate=datetime.utcnow,
    )

    def __str__(self):
        return f"{self.__tablename__}:{self.id}"

    def __repr__(self):
        try:
            return f"{self.__class__.__name__}({self.__tablename__}:{self.id})"
        except:
            return f"Faulty-{self.__class__.__name__}"

    @property
    def created_jalali(self):
        created = (self.created).replace(tzinfo=None)
        utc = datetime.strptime(str(created), "%Y-%m-%d %H:%M:%S.%f")
        created_hour = "{:0>2}".format(int(utc.hour))
        created_minute = "{:0>2}".format(int(utc.minute))
        created_second = "{:0>2}".format(int(utc.second))
        created_time = created_hour + ":" + created_minute + ":" + created_second
        return JalaliDate(utc).strftime("%Y-%m-%d") + " " + created_time
