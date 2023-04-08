from sqlalchemy.ext.asyncio import AsyncSession

from db.base import db
from db.crud import BetCrud
from db.schemas import Event


async def up_bets(event: Event) -> None:
    db_session: AsyncSession = db.async_sessionmaker()  # type: ignore
    await BetCrud(db_session).update_bet(event_id=event.event_id, status=event.status)
    await db_session.commit()
    await db_session.close()
