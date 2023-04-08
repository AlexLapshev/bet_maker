import asyncio
import uuid

import uvicorn as uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import utils.events.utils
from db.base import db
from db.crud import BetCrud
from db.schemas import BetSchema, BetBaseSchema, Event
from rabbit.client import Rabbit

app = FastAPI()
rmq = Rabbit()


@app.on_event("startup")
def startup() -> None:
    db.setup()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rmq.setup(loop))
    asyncio.ensure_future(rmq.consume_messages())


@app.post("/bet", status_code=201)
async def create_bet(
    bet: BetBaseSchema, db_session: AsyncSession = Depends(db)
) -> uuid.UUID:
    # не было в задании, можно проверять на фронте
    if await utils.events.utils.check_bet_for_outdated(bet):
        raise HTTPException(status_code=409, detail="Event is outdated")
    return await BetCrud(db_session).add(bet)


@app.get("/bets")
async def get_event(db_session: AsyncSession = Depends(db)) -> list[BetSchema]:
    bets = await BetCrud(db_session).get_all()
    return bets


@app.get("/events", status_code=200)
async def get_events() -> list[Event]:
    return await utils.events.utils.get_events()


if __name__ == "__main__":
    uvicorn.run(app=app, port=8001, host="0.0.0.0")
