from app.users.repository import UserRepository
from app.auth.common.types import AuthProvider
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class PasswordAuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, email: str, password: str) -> str:
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("User already exists")

        password_hash = hash_password(password)

        user = await self.user_repo.create(
            email=email,
            password_hash=password_hash,
            auth_provider=AuthProvider.PASSWORD,
        )

        return create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role},
        )

    async def login(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user or not user.password_hash:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("User is inactive")

        return create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role},
        )
