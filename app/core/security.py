from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt
    """
    return password_hash.hash(password=password)


def verify_password(plain_password, hashed_password):
    """
    Verify a password against a hashed password
    """
    return password_hash.verify(password=plain_password, hash=hashed_password)
