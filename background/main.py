import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO
from dramatiq.middleware import CurrentMessage

from background import config
from background.middlewares import Logger

broker = RedisBroker(url=config.broker_redis_url)
dramatiq.set_broker(broker)
dramatiq.get_broker().add_middleware(AsyncIO())
dramatiq.get_broker().add_middleware(CurrentMessage())
dramatiq.get_broker().add_middleware(Logger())

import background.tasks
