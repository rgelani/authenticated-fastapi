from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import aiosqlite

from app.core.security import decode_access_token
from app.db.database import get_db
from app.users.repository import UserRepository
from app.users.model import User
from app.auth.common.types import UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/password/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: aiosqlite.Connection = Depends(get_db),
) -> User:
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    repo = UserRepository(db)
    user = await repo.get_by_id(int(user_id))

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    return user

def require_role(required_role: UserRole) -> Callable:
    async def role_checker(
        user: User = Depends(get_current_user),
    ) -> User:
        if user.role != required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return role_checker
