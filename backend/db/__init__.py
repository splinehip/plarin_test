import motor.motor_asyncio

from settings import settings


class Database():
    def __init__(self) -> None:
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.MONGODB_URL)
        self.database = self.client.plarin_test
        self.user_collection = self.database.get_collection("user")
