import decimal
import time
import uuid
from copy import copy
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient

from app import app, rmq
from db.base import db
from db.models import Status
from db.schemas import BetSchema

result = [
    BetSchema(
        id=uuid.UUID("f2f817e1-42bf-42fd-b11c-fac4514a9c96"),
        status=Status.NEW,
        event_id=1,
        amount=13.13),  # type: ignore
    BetSchema(
        id=uuid.UUID("f2f817e1-42bf-42fd-b11c-fac4514a9c97"),
        status=Status.NEW,
        event_id=23,
        amount=12.12),  # type: ignore
]


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


app.dependency_overrides[rmq] = lambda: AsyncMock()
app.dependency_overrides[db] = lambda: AsyncMock()
dummy_id = uuid.UUID("f2f817e1-42bf-42fd-b11c-fac4514a9c97")


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_simple_workflow(anyio_backend):
    test_event = {
        "event_id": 23,
        "amount": 12.12,
    }

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        create_response = await ac.post("/bet", json=test_event)

    assert create_response.status_code == 201
    assert create_response.json() == str(dummy_id)

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        get_response = await ac.get("/bets")

    assert get_response.status_code == 200
    assert [BetSchema(**b) for b in get_response.json()] == result
