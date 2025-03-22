from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt.

    :param password: The plaintext password to hash.
    :return: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a hashed password.

    :param plain_password: The plaintext password.
    :param hashed_password: The hashed password stored in the database.
    :return: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
