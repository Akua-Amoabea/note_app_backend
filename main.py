from typing import List
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from routes.v1 import notes
from config.database import engine, Base
from routes.v1.users import user_router

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user_router)
app.include_router(notes.router)

