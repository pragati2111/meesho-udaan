from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

_client: AsyncIOMotorClient | None = None


async def connect_db() -> None:
    global _client
    _client = AsyncIOMotorClient(settings.MONGODB_URI)
    # Verify connection
    await _client.admin.command("ping")
    print("✅ Connected to MongoDB Atlas")


async def disconnect_db() -> None:
    global _client
    if _client:
        _client.close()
        print("🔌 Disconnected from MongoDB")


def get_db() -> AsyncIOMotorDatabase:
    if _client is None:
        raise RuntimeError("Database not connected. Call connect_db() first.")
    return _client[settings.MONGODB_DB_NAME]