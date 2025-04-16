from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.ME_CONFIG_MONGODB_URL)
        self.db = self.client[settings.MONGO_INITDB_DATABASE]

    async def disconnect(self):
        if self.client:
            self.client.close()


mongodb = MongoDB()
