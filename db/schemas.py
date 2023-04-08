import decimal
import uuid
from typing import Optional, Any

from pydantic import BaseModel, validator

from db.models import Status


class BetBaseSchema(BaseModel):
    event_id: int
    amount: decimal.Decimal

    @validator("amount", pre=True)
    def validate_amount(cls, v: Any) -> decimal.Decimal:
        s = str(v).split(".")
        if len(s) != 2 or len(s[-1]) > 2 or v <= 0:
            raise ValueError("Incorrect amount")
        return v


class BetSchema(BetBaseSchema):
    id: Optional[uuid.UUID]
    status: Optional[Status]


class Event(BaseModel):
    event_id: str
    status: Status
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[int] = None
