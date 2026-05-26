from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

_client: AsyncIOMotorClient = None


async def connect_db():
    global _client
    _client = AsyncIOMotorClient(settings.mongodb_uri)


async def close_db():
    global _client
    if _client:
        _client.close()


def get_db():
    return _client[settings.mongodb_db]
