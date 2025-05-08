# db/init_db.py

from api.db import async_engine, Base
from api.user.models import * 

async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)