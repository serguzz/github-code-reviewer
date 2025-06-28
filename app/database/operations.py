"""
Database operations for PR reviews
"""
import sqlite3
from typing import List, Optional

from ..config.settings import DB_FILE
from ..models.database import ReviewComment, PR_REVIEWS_TABLE_SQL, REVIEW_COMMENTS_TABLE_SQL

class DatabaseOperations:
    """Handle all database operations"""
    
    @staticmethod
    def init_database():
        """Initialize SQLite database"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute(PR_REVIEWS_TABLE_SQL)
        cursor.execute(REVIEW_COMMENTS_TABLE_SQL)
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def store_review_data(
        pr_url: str, 
        repo_name: str, 
        pr_number: int, 
        status: str, 
        comments: Optional[List[ReviewComment]] = None, 
        error_message: Optional[str] = None
    ) -> int:
        """Store review data in database"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Insert PR review record
        cursor.execute("""
            INSERT INTO pr_reviews (pr_url, repo_name, pr_number, status, comments_added, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pr_url, repo_name, pr_number, status, len(comments) if comments else 0, error_message))
        
        review_id = cursor.lastrowid
        if review_id is None:
            raise ValueError("Failed to insert review record")
        
        # Insert individual comments
        if comments:
            for comment in comments:
                cursor.execute("""
                    INSERT INTO review_comments (pr_review_id, file_path, line_number, comment)
                    VALUES (?, ?, ?, ?)
                """, (review_id, comment.file_path, comment.line_number, comment.comment))
        
        conn.commit()
        conn.close()
        
        return review_id
    
    @staticmethod
    def get_recent_reviews(limit: int = 20) -> List[dict]:
        """Get recent reviews from database"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT pr_url, repo_name, pr_number, status, created_at, comments_added
            FROM pr_reviews
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        reviews = []
        for row in cursor.fetchall():
            reviews.append({
                "pr_url": row[0],
                "repo_name": row[1],
                "pr_number": row[2],
                "status": row[3],
                "created_at": row[4],
                "comments_added": row[5]
            })
        
        conn.close()
        return reviews 