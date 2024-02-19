# ------------- dependences ------------- #
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.future import select
from sqlalchemy import delete, update
from configuration import DATABASE_FILENAME
# ------------- ----------- ------------- #

async_engine = create_async_engine(f'sqlite+aiosqlite:///{DATABASE_FILENAME}') # sqlite:///{DATABASE_FILENAME}
async_session = async_sessionmaker(async_engine, expire_on_commit = False)

# ------------- ------ ------------- #
class Base(AsyncAttrs, DeclarativeBase):
    pass
# ------------- ------ ------------- #

# ------------- ------ ------------- #
class Moderator(Base):
    __tablename__ = 'moderators'
    
    id               = Column(Integer, primary_key = True)
    telegram_user_id = Column(Integer, nullable = False)
# ------------- ------ ------------- #

# ------------- ------ ------------- #
class User(Base):
    __tablename__ = 'users'
    
    id               = Column(Integer, primary_key = True)
    telegram_user_id = Column(Integer, nullable = False)
    is_banned        = Column(Boolean, default = False)
# ------------- ------ ------------- #

# ------------- ------ ------------- #
class Question(Base):
    __tablename__ = 'questions'
    
    id               = Column(Integer, primary_key = True)
    user_id          = Column(Integer, nullable = False)
    text             = Column(String,  nullable = False)
    answer_id        = Column(Integer, nullable = True)
# ------------- ------ ------------- #

# ------------- ------ ------------- #
class Answer(Base):
    __tablename__ = 'answers'
    
    id          = Column(Integer, primary_key = True)
    user_id     = Column(Integer, nullable = False)
    question_id = Column(Integer, nullable = False)
    text        = Column(String, nullable = False)
# ------------- ------ ------------- #

# additional functions

async def fetchone(stmt, session):
    result = await session.execute(stmt)
    return result.scalar()

async def fetchmany(stmt, session):
    result = await session.execute(stmt)
    return result.scalars()

async def insert(object_, session):
    session.add(object_)
    await session.commit()
    
async def execute_stmt(stmt, session) -> None:
    await session.execute(stmt)
    await session.commit()