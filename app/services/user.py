from core.security import hash_password
from repositories.user import find_user_by_username, insert_user, update_user
from schemas.user import User, UserCreate, UserInDB


async def get_user(username: str) -> User | None:
    """
    Get user by username
    """
    user = await find_user_by_username(username=username)
    return User(**user.model_dump(exclude={"hashed_password"})) if user else None


async def get_user_in_db(username: str) -> UserInDB | None:
    """
    Get user by username from the database
    """
    return await find_user_by_username(username=username)


async def create_user(user: UserCreate) -> User | None:
    """
    Create user in the database
    """
    hashed_password = hash_password(password=user.password)
    user_in_db = UserInDB(
        **user.model_dump(exclude={"password"}), hashed_password=hashed_password
    )
    user = await insert_user(user=user_in_db)
    return User(**user.model_dump(exclude={"hashed_password"})) if user else None


async def change_password(user: User, new_password: str) -> User | None:
    """
    Change user password
    """
    hashed_password = hash_password(password=new_password)
    user_in_db = UserInDB(
        **user.model_dump(exclude={"password"}), hashed_password=hashed_password
    )
    user = await update_user(user=user_in_db)
    return User(**user.model_dump(exclude={"hashed_password"})) if user else None
