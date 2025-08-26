from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from dotenv import load_dotenv


load_dotenv()

URL_DATABASE = str(os.getenv('ASYNC_URL_DATABASE'))

# create async engine
engine = create_async_engine(URL_DATABASE, echo=True)

# create session fabric
AsyncSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# base class for models
Base = declarative_base()