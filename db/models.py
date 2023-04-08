import enum
import uuid

from sqlalchemy import Column, Integer, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum

from db.base import Base


class Status(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class Bet(Base):
    __tablename__ = "bets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(Integer, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)  # type: ignore
    status = Column(Enum(Status), nullable=False, default=Status.NEW)  # type: ignore
    # created_at - не было в задании
