from fastapi import APIRouter, Depends, HTTPException, status
import aiosqlite

from app.db.database import get_db
from app.users.repository import UserRepository
from app.auth.password.schemas import RegisterRequest, LoginRequest
from app.auth.password.service import PasswordAuthService
from app.auth.common.schemas import TokenResponse


router = APIRouter(prefix="/auth/password", tags=["Password Auth"])


def get_auth_service(db: aiosqlite.Connection = Depends(get_db)) -> PasswordAuthService:
    user_repo = UserRepository(db)
    return PasswordAuthService(user_repo)


@router.post("/register", response_model=TokenResponse)
async def register(
    data: RegisterRequest,
    service: PasswordAuthService = Depends(get_auth_service),
):
    try:
        token = await service.register(data.email, data.password)
        return TokenResponse(access_token=token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    service: PasswordAuthService = Depends(get_auth_service),
):
    try:
        token = await service.login(data.email, data.password)
        return TokenResponse(access_token=token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
