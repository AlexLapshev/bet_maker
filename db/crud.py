import uuid

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Bet, Status
from db.schemas import BetSchema, BetBaseSchema


class BetCrud:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get(self, bet_id: str) -> BetSchema:
        bet = await self.db_session.execute(select(Bet).where(Bet.id == bet_id))  # type: ignore
        return BetSchema(**bet.__dict__)

    async def get_all(self) -> list[BetSchema]:
        bets = await self.db_session.execute(select(Bet))
        return [BetSchema(**b.__dict__) for b in bets.scalars()]

    async def add(self, bet: BetBaseSchema) -> uuid.UUID:
        uuid_ = uuid.uuid4()
        q = insert(Bet).values(
            {"id": uuid_, **bet.dict()}
        )
        await self.db_session.execute(q)
        return uuid_

    async def update_bet(self, event_id: str, status: Status) -> None:
        q = (
            update(Bet)
            .values({"status": status.name})
            .where(Bet.event_id == int(event_id))
        )
        await self.db_session.execute(q)
