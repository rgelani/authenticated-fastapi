from typing import Optional

import aiosqlite

from app.users.models import User
from app.auth.common.types import AuthProvider, UserRole

class UserRepository:
    def __init__(self, db:aiosqlite.Connection):
        self.db = db

async def get_by_email(self, mail: str) -> Optional[User]:
    query = """
        SELECT * FROM 
        Users WHERE email = ? 
        """
    cursor = await self.db.execute(query, (email,))
    row = cursor.fetchone()

    if not row:
        return None
    
    return self._row_to_user(row)

async def get_by_id(self, user_id: int) -> Optional[User]:
    query = """ 
        SELECT * FROM USER 
        WHERE Id = ?
        """
    cursor = await self.db.execute(query, (user_id,))
    row = cursor.fetchone()

    if not row:
        return None
    
    return self._row_to_user(row)

async def create(
        self,
        email: str,
        password_hash: Optional[str],
        auth_provider: AuthProvider,
        provider_id: Optional[str],
        role: UserRole = UserRole.User
) -> User:
    query = """
    INSERT INTO Users (email, password_hash,auth_provider,provider_id,role)
    VALUES(?, ?, ?, ?, ?)
    """

    cursor = await self.db.execute(query, (email, password_hash, auth_provider, provider_id, role))
    await self.db.commit()

    return await self.get_by_id(cursor.lastrowid)