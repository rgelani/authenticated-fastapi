from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import Settings

pwd_context = CryptContext(schema=["bcrypt"], deprecated="auto")

# --------------------
# Password utilities
# --------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)

# --------------------
# JWT utilities
# --------------------

def create_access_token (
    subject: str,
    expires_delta: Optional[timedelta] = None,
    extra_claims = Optional[dict] = None,
) -> str:  
    payload = {"sub": subject}

    if extra_claims:
        payload.update(extra_claims)

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload, 
        Settings.SECRET_KEY, 
        algorithm=Settings.ALGORITHM
    )

def decode_jwt_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            Settings.SECRET_KEY,
            algorithms=[Settings.ALGORITHM],
        )
    except JWTError:
        return {}