import uuid
from unittest.mock import MagicMock

import rabbit.client
import db.base
import db.crud
import utils.events.utils
from db.models import Status
from db.schemas import BetSchema, BetBaseSchema

dummy_id = uuid.UUID("f2f817e1-42bf-42fd-b11c-fac4514a9c97")


async def return_true(*args, **kwargs):
    return False


class BetCrudDummy:
    bets = [
        BetSchema(
            id=uuid.UUID("f2f817e1-42bf-42fd-b11c-fac4514a9c96"),
            status=Status.NEW,
            event_id=1,
            amount=13.13  # type: ignore
        )
    ]

    def __init__(self, *args, **kwargs):
        pass

    async def get(self, bet_id: str) -> BetSchema:
        return [b for b in self.bets if b.id == uuid.UUID(bet_id)][0]

    async def get_all(self) -> list[BetSchema]:
        return self.bets

    async def add(self, bet: BetBaseSchema) -> uuid.UUID:
        self.bets.append(BetSchema(**bet.dict(), id=dummy_id, status=Status.NEW))
        return dummy_id

    async def update_bet(self, event_id: str, status: Status) -> None:
        pass


rabbit.client.Rabbit = MagicMock
db.base.PostgresDatabase = MagicMock
db.crud.BetCrud = BetCrudDummy
utils.events.utils.check_bet_for_outdated = return_true
