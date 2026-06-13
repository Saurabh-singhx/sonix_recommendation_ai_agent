from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import connect_db, disconnect_db
from app.api.v1.recommendation import router as rec_router

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()    # runs on startup
    print("db Connected...")
    yield
    await disconnect_db() # runs on shutdown
    print("db Disconnected...")

app = FastAPI(lifespan=lifespan)

app.include_router(rec_router, prefix="/api/v1")
