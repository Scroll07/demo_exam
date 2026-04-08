from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def create_hash(password: str) -> str:
    password_hash = pwd_context.hash(password)
    return password_hash

def verify_hash(password: str, password_hash: str) -> bool:
    is_right_password = pwd_context.verify(password, password_hash)
    return is_right_password