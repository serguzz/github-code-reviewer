"""
FastAPI routes for the GitHub PR Review Bot
"""
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..models.schemas import PRReviewRequest, PRReviewResponse
from ..services.review_service import ReviewService
from ..database.operations import DatabaseOperations
from ..utils.github_utils import parse_github_url

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize templates
templates = Jinja2Templates(directory="app/templates")

# Initialize services
review_service = ReviewService()
db_ops = DatabaseOperations()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with simple form"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/reviews", response_class=HTMLResponse)
async def reviews_page(request: Request):
    """Reviews page to view all reviews"""
    return templates.TemplateResponse("reviews.html", {"request": request})

@router.post("/review", response_model=PRReviewResponse)
async def review_pr(request: PRReviewRequest):
    """Review a GitHub PR"""
    logger.info(f"Received review request for: {request.pr_url}")
    
    # Validate URL format
    try:
        parse_github_url(request.pr_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Process review
    result = await review_service.process_pr_review(request.pr_url)
    
    if result["status"] == "failed":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return PRReviewResponse(
        status=result["status"],
        message=result["message"],
        review_id=result.get("review_id")
    )

@router.get("/api/reviews")
async def get_reviews():
    """Get recent reviews"""
    reviews = db_ops.get_recent_reviews()
    return {"reviews": reviews}

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()} 