# pyright: reportCallIssue=false, reportArgumentType=false, reportGeneralTypeIssues=false, reportReturnType=false

import os
from typing import Protocol

from fastapi import FastAPI, Request

from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the SQLAlchemy engine for async
SQLALCHEMY_DATABASE_URL = os.environ["DB_CONNECTION"]
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Page size for paged API
PAGE_SIZE = 30

# Limit for non-paged queries
NON_PAGED_LIMIT = 300

# Create a configured "AsyncSession" class
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)

class ORMObject(Protocol):
    __table__: Table

# Base class for SQLAlchemy models
Base : ORMObject = declarative_base()

# Dependency to get the database session
async def get_db(request : Request):
    yield request.state.db

def add_db_middleware(app : FastAPI):
    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        async with async_session() as session:
            request.state.db = session
            try:
                response = await call_next(request)
                await session.commit()
                return response
            except:
                await session.rollback()
                raise

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)