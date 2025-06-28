"""
Pydantic models for request/response schemas
"""
from typing import Optional
from pydantic import BaseModel

class PRReviewRequest(BaseModel):
    """Request model for PR review"""
    pr_url: str

class PRReviewResponse(BaseModel):
    """Response model for PR review"""
    status: str
    message: str
    review_id: Optional[int] = None

class ReviewData(BaseModel):
    """Review data for API responses"""
    pr_url: str
    repo_name: str
    pr_number: int
    status: str
    created_at: str
    comments_added: int 