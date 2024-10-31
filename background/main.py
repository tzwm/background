import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO
from dramatiq.middleware import CurrentMessage

from background import config
from background.middlewares import Logger

broker = RedisBroker(
    url=config.broker_redis_url,
    middleware=[
        AsyncIO(),
        CurrentMessage(),
        Logger(),
    ],
)
dramatiq.set_broker(broker)

import background.tasks
