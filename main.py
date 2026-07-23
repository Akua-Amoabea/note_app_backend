from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.v1 import notes
from routes.v1.users import user_router
from routes.v1.auth import auth_router
from services.apscheduler_services import run_scheduler



@asynccontextmanager
async def lifespan(app: FastAPI):
    run_scheduler()
    yield


app = FastAPI(lifespan=lifespan, title="Note - API", version="0.1.0"
)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(notes.router)


