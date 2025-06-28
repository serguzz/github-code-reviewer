#!/usr/bin/env python3
"""
Entry point for the GitHub PR Review Bot
"""
import uvicorn
from app.config.settings import HOST, PORT

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True) 