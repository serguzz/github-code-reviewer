"""
Configuration settings for the GitHub PR Review Bot
"""
import os
import logging
import dotenv

# AI Model Configuration
MODEL = "gpt-4o-mini"  # gpt-4o-mini, gpt-4o, gpt-4

# Environment Variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database Configuration
DB_FILE = "pr_reviews.db"

# Application Settings
APP_TITLE = "GitHub PR Review Bot"
APP_VERSION = "1.0.0"
HOST = "127.0.0.1"
PORT = 8000

# Logging Configuration
LOG_FILE = "pr_review_bot.log"
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

dotenv.load_dotenv()

def validate_environment():
    """Validate required environment variables"""
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__) 