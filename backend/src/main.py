from typing import Annotated
from fastapi import FastAPI, Cookie

from util.logging import setup_logging

from api import auth, users
from core.database import add_db_middleware

setup_logging()
app = FastAPI()
add_db_middleware(app)
auth.include_routers(app)
users.include_routers(app)

@app.get("/api")
async def root(ads_id: Annotated[str | None, Cookie()] = None):
    return {"message": f"Hello World Cookie={ads_id}"}

