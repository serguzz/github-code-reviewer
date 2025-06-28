"""
Main review service that orchestrates the PR review process
"""
import logging
from typing import Dict, Any

from ..services.github_service import GitHubService
from ..services.ai_service import AIService
from ..database.operations import DatabaseOperations
from ..utils.github_utils import parse_github_url

logger = logging.getLogger(__name__)

class ReviewService:
    """Main service for orchestrating PR reviews"""
    
    def __init__(self):
        """Initialize services"""
        self.github_service = GitHubService()
        self.ai_service = AIService()
        self.db_ops = DatabaseOperations()
    
    async def process_pr_review(self, pr_url: str) -> Dict[str, Any]:
        """Process PR review end-to-end"""
        logger.info(f"Starting review for PR: {pr_url}")
        
        try:
            # Parse GitHub URL
            repo_name, pr_number = parse_github_url(pr_url)
            logger.info(f"Parsed PR: {repo_name}#{pr_number}")
            
            # Check if PR exists and get PR from GitHub
            try:
                pr, repo_name, pr_number = self.github_service.get_pull_request(pr_url)
                logger.info(f"Found PR: {pr.title}")
            except Exception as e:
                error_msg = ""
                if "404" in str(e) or "Not Found" in str(e):
                    error_msg = f"Pull Request not found: {repo_name}#{pr_number}. Please check the URL and ensure the PR exists and is accessible."
                elif "403" in str(e) or "Forbidden" in str(e):
                    error_msg = f"Access denied to PR {repo_name}#{pr_number}. Please check if the repository is private or requires authentication."
                else:
                    error_msg = f"Failed to access PR {repo_name}#{pr_number}: {str(e)}"
                
                logger.warning(f"PR access failed: {error_msg}")
                
                # Store as client error in database
                review_id = self.db_ops.store_review_data(
                    pr_url, repo_name, pr_number, "invalid", None, error_msg
                )
                
                return {
                    "status": "invalid",
                    "message": error_msg,
                    "review_id": review_id
                }
            
            # Get PR details
            pr_details = self.github_service.get_pr_details(pr)
            pr_title = pr_details['title']
            pr_body = pr_details['body']
            pr_files = pr_details['files']
            
            logger.info(f"Found {len(pr_files)} modified files")
            
            if not pr_files:
                review_id = self.db_ops.store_review_data(
                    pr_url, repo_name, pr_number, "completed", [], "No files to review"
                )
                return {
                    "status": "completed", 
                    "message": "No files to review", 
                    "review_id": review_id
                }
            
            # Analyze code with AI
            logger.info("Analyzing code with AI...")
            comments = self.ai_service.analyze_code_with_ai(pr_files, pr_title, pr_body)
            logger.info(f"Generated {len(comments)} review comments")
            
            # Add comments to PR
            if comments:
                added_comments = self.github_service.add_review_comments_to_pr(pr, comments)
                logger.info(f"Added {added_comments} comments to PR")
            else:
                added_comments = 0
                logger.info("No issues found - no comments added")
            
            # Store in database
            review_id = self.db_ops.store_review_data(pr_url, repo_name, pr_number, "completed", comments)
            
            return {
                "status": "completed",
                "message": f"Review completed. Added {added_comments} comments.",
                "review_id": review_id,
                "comments_count": len(comments)
            }
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error processing PR review: {error_msg}")
            
            # Store error in database
            try:
                repo_name, pr_number = parse_github_url(pr_url)
                review_id = self.db_ops.store_review_data(
                    pr_url, repo_name, pr_number, "failed", None, error_msg
                )
            except:
                review_id = None
            
            return {
                "status": "failed",
                "message": f"Review failed: {error_msg}",
                "review_id": review_id
            } 