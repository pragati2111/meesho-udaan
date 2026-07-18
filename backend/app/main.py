from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import connect_db, disconnect_db
from app.core.logging import setup_logging
from app.api.routes import health, business, upload


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await connect_db()
    yield
    await disconnect_db()


app = FastAPI(
    title="Meesho Udaan API",
    description="The Entrepreneur Discovery Engine for Bharat",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(business.router, prefix="/api/business", tags=["Business"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])