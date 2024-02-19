# ------------- dependences ------------- #
from database import Base, Moderator, async_engine, async_session
import asyncio
# ------------- ----------- ------------- #

moderator_id = int(input('paste here moderator id -> '))

async def main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session() as session:
        session.add(Moderator(telegram_user_id = moderator_id))
        await session.commit()

asyncio.run(main())