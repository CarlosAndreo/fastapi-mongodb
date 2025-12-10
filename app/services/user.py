from core.security import get_password_hash
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
    hashed_password = get_password_hash(password=user.password)
    user_in_db = UserInDB(
        **user.model_dump(exclude={"password"}), hashed_password=hashed_password
    )
    created_user = await insert_user(user=user_in_db)
    return User(**created_user.model_dump(exclude={"hashed_password"})) if created_user else None


async def change_password(user: User, new_password: str) -> User | None:
    """
    Change user password
    """
    hashed_password = get_password_hash(password=new_password)
    user_in_db = UserInDB(
        **user.model_dump(exclude={"password"}), hashed_password=hashed_password
    )
    updated_user = await update_user(user=user_in_db)
    return User(**updated_user.model_dump(exclude={"hashed_password"})) if updated_user else None
