import asyncio
import decimal
import random

from sqlalchemy.ext.asyncio import AsyncSession

from db.base import PostgresDatabase
from db.crud import BetCrud
from db.schemas import BetBaseSchema


async def insert_100_bets(session: AsyncSession) -> None:
    for i in range(1, 101):
        s = BetBaseSchema(
            amount=decimal.Decimal(
                f"{random.randint(100, 500)}.{random.randint(11, 99)}"
            ),
            event_id=random.randint(1, 3),
        )
        await BetCrud(session).add(s)
    await session.commit()
    print("SUCCESSFULLY INSERTED 100 BETS")


async def main(postgres_db: PostgresDatabase):
    async_gen_session = postgres_db()
    session = await anext(async_gen_session)
    await insert_100_bets(session)


if __name__ == "__main__":
    db = PostgresDatabase()
    db.setup(echo=False)
    asyncio.run(main(db))
