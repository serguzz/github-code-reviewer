"""
Main FastAPI application for GitHub PR Review Bot
"""
import logging
from fastapi import FastAPI

from .config.settings import APP_TITLE, APP_VERSION, setup_logging, validate_environment
from .database.operations import DatabaseOperations
from .api.routes import router

# Setup logging
logger = setup_logging()

# Validate environment
validate_environment()

# Create FastAPI app
app = FastAPI(title=APP_TITLE, version=APP_VERSION)

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    DatabaseOperations.init_database()
    logger.info("PR Review Bot started") 