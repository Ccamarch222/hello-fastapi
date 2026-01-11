from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.routers import task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    create_db_and_tables()
    yield


app = FastAPI(
    title="Task Management API",
    description="A complete CRUD API for managing tasks",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Welcome to Task Management API"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include routers
app.include_router(task_router)
