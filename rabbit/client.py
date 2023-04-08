import json
from asyncio import AbstractEventLoop

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from config.settings import QueueSettings
from db.schemas import Event
from rabbit.utils import up_bets


class Rabbit:
    connection_pool = None
    channel_pool = None

    def __init__(self, settings: QueueSettings = QueueSettings()):
        self.settings = settings

    async def __call__(self) -> "Rabbit":
        if not self.channel_pool:
            raise ValueError("channel_pool not available. Run setup() first.")
        return self

    async def setup(self, loop: AbstractEventLoop) -> None:
        self.connection_pool: Pool = Pool(self.get_connection, max_size=2, loop=loop)  # type: ignore
        self.channel_pool: Pool = Pool(self.get_channel, max_size=10, loop=loop)  # type: ignore

    async def get_connection(self) -> AbstractRobustConnection:
        return await aio_pika.connect_robust(
            f"amqp://{self.settings.username}:{self.settings.password}@{self.settings.host}/"
        )

    async def get_channel(self) -> aio_pika.Channel:
        async with self.connection_pool.acquire() as connection:  # type: ignore
            return await connection.channel()

    async def consume_messages(self) -> None:
        async with self.channel_pool.acquire() as channel:  # type: ignore
            queue: aio_pika.Queue = await channel.declare_queue(
                QueueSettings.queue_name_events, auto_delete=False
            )  # type: ignore
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():  # type: ignore
                        j = json.loads(message.body)  # type: ignore
                        event = Event(**j)
                        print(event.dict())
                        await up_bets(event)
                        await self.publish(json.dumps({"result": "success"}))

    async def publish(self, message: str) -> None:
        async with self.channel_pool.acquire() as channel:  # type: ignore
            await channel.default_exchange.publish(
                aio_pika.Message(message.encode()),
                self.settings.queue_name_bets,
            )
