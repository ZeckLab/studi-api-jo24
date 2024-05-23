from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import jwt

from src.core.config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_keygen_hash(email: str) -> str:
    return pwd_context.hash(email)

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGO)
    return encoded_jwt