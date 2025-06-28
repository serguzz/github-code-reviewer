"""
Database models and structures
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ReviewComment:
    """Review comment data structure"""
    file_path: str
    line_number: int
    comment: str

@dataclass
class PRReview:
    """PR Review data structure"""
    id: Optional[int] = None
    pr_url: str = ""
    repo_name: str = ""
    pr_number: int = 0
    status: str = ""
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    comments_added: int = 0
    error_message: Optional[str] = None

# Database schema definitions
PR_REVIEWS_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS pr_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pr_url TEXT NOT NULL,
        repo_name TEXT NOT NULL,
        pr_number INTEGER NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        comments_added INTEGER DEFAULT 0,
        error_message TEXT
    )
"""

REVIEW_COMMENTS_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS review_comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pr_review_id INTEGER,
        file_path TEXT NOT NULL,
        line_number INTEGER,
        comment TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pr_review_id) REFERENCES pr_reviews (id)
    )
""" 