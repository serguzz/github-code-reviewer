"""
Main FastAPI application for GitHub PR Review Bot
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config.settings import APP_TITLE, APP_VERSION, setup_logging, validate_environment
from .database.operations import DatabaseOperations
from .api.routes import router

# Setup logging
logger = setup_logging()

# Validate environment
validate_environment()

# Create FastAPI app
app = FastAPI(title=APP_TITLE, version=APP_VERSION)

# Mount static files
app.mount("/static", StaticFiles(directory="app/templates"), name="static")

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    DatabaseOperations.init_database()
    logger.info("PR Review Bot started") 