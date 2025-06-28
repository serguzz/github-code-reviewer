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
    def fix_database():
        """Fix/repair database by recreating tables if needed"""
        import os
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # Test database connection
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            # Check if tables exist and have correct structure
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['pr_reviews', 'review_comments']
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                logger.warning(f"Missing tables: {missing_tables}. Recreating...")
                # Recreate missing tables
                cursor.execute(PR_REVIEWS_TABLE_SQL)
                cursor.execute(REVIEW_COMMENTS_TABLE_SQL)
                conn.commit()
                logger.info("Database tables recreated successfully")
            
            # Verify table structures
            for table in expected_tables:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                logger.info(f"Table {table} has {len(columns)} columns")
            
            conn.close()
            logger.info("Database integrity check completed")
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            # If there's a corruption, try to backup and recreate
            try:
                if os.path.exists(DB_FILE):
                    backup_file = f"{DB_FILE}.backup"
                    os.rename(DB_FILE, backup_file)
                    logger.info(f"Corrupted database backed up to {backup_file}")
                
                # Recreate database
                DatabaseOperations.init_database()
                logger.info("Database recreated from scratch")
                return True
                
            except Exception as backup_error:
                logger.error(f"Failed to fix database: {backup_error}")
                return False
        
        except Exception as e:
            logger.error(f"Unexpected error during database fix: {e}")
            return False
    
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
            SELECT id, pr_url, repo_name, pr_number, status, created_at, comments_added
            FROM pr_reviews
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        reviews = []
        for row in cursor.fetchall():
            reviews.append({
                "id": row[0],
                "pr_url": row[1],
                "repo_name": row[2],
                "pr_number": row[3],
                "status": row[4],
                "created_at": row[5],
                "comments_added": row[6]
            })
        
        conn.close()
        return reviews
    

    @staticmethod
    def get_comments_for_review(review_id: int) -> List[ReviewComment]:
        """Get comments for a review"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT file_path, line_number, comment
            FROM review_comments
            WHERE pr_review_id = ?
        """, (review_id,))
        
        comments = []
        for row in cursor.fetchall():
            comments.append(ReviewComment(
                file_path=row[0],
                line_number=row[1],
                comment=row[2]
            ))
        
        conn.close()
        return comments
    
    @staticmethod
    def get_review_details(review_id: int) -> Optional[dict]:
        """Get review details by ID"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, pr_url, repo_name, pr_number, status, created_at, comments_added, error_message
            FROM pr_reviews
            WHERE id = ?
        """, (review_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "pr_url": row[1],
                "repo_name": row[2],
                "pr_number": row[3],
                "status": row[4],
                "created_at": row[5],
                "comments_added": row[6],
                "error_message": row[7]
            }
        return None