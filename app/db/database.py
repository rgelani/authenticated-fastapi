import aiosqlite
from typing import AsyncGenerator

from app.core.config import settings

DATABASE_URL = settings.SQLITE_DB_PATH

async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    """
    Provides a SQLite connection per request.
    This is intentionally simple and explicit.
    """

    db = await aiosqlite.connect(DATABASE_URL)
    db.row_factory = aiosqlite.Row

    try:
        yield db
    finally:
        db.close()    
