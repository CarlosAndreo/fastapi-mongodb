from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    """
    return pwd_context.hash(secret=password)


def verify_password(plain_password, hashed_password):
    """
    Verify a password against a hashed password
    """
    return pwd_context.verify(secret=plain_password, hash=hashed_password)
