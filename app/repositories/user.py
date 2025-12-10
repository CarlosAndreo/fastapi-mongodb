from database.mongodb import mongodb
from schemas.user import UserInDB


def get_collection():
    """
    Collection for user
    """
    return mongodb.db["users"]  # type: ignore


async def find_user_by_username(username: str) -> UserInDB | None:
    """
    Find user by username in the database
    """
    user = await get_collection().find_one({"username": username})
    return UserInDB(**user) if user else None


async def insert_user(user: UserInDB) -> UserInDB | None:
    """
    Insert user in the database
    """
    await get_collection().insert_one(user.model_dump())
    return user if user else None


async def update_user(user: UserInDB) -> UserInDB | None:
    """
    Update user in the database
    """
    await get_collection().update_one(
        {"username": user.username}, {"$set": user.model_dump()}
    )
    return user if user else None
