import time

import httpx
from fastapi import HTTPException

from config.settings import LINE_PROVIDER_URL
from db.schemas import Event, BetBaseSchema


async def get_event(event_id: str) -> Event:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{LINE_PROVIDER_URL}/event/{event_id}")
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="Event not found")
        event = r.json()
        return Event(**event)


async def get_events() -> list[Event]:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{LINE_PROVIDER_URL}/events")
        events = [Event(**e) for e in r.json()]
        return events


async def check_bet_for_outdated(bet: BetBaseSchema) -> bool:
    t_now = int(time.time())
    event = await get_event(bet.event_id)  # type: ignore
    return t_now >= event.deadline
