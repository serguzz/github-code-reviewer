"""
GitHub API service for managing PR operations
"""
import logging
from typing import List
from github import Github
from github.PullRequest import PullRequest

from ..config.settings import GITHUB_TOKEN
from ..models.database import ReviewComment
from ..utils.github_utils import parse_github_url, get_pr_files

logger = logging.getLogger(__name__)

class GitHubService:
    """Service for GitHub API operations"""
    
    def __init__(self):
        """Initialize GitHub client"""
        self.client = Github(GITHUB_TOKEN)
    
    def get_pull_request(self, pr_url: str) -> tuple[PullRequest, str, int]:
        """Get PR object from GitHub URL"""
        repo_name, pr_number = parse_github_url(pr_url)
        repo = self.client.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        return pr, repo_name, pr_number
    
    def get_pr_details(self, pr: PullRequest) -> dict:
        """Extract PR details"""
        return {
            'title': pr.title,
            'body': pr.body,
            'files': get_pr_files(pr)
        }
    
    def add_review_comments_to_pr(self, pr: PullRequest, comments: List[ReviewComment]) -> int:
        """Add review comments to GitHub PR"""
        if not comments:
            return 0
        
        # Get the latest commit SHA
        commits = list(pr.get_commits())
        if not commits:
            raise ValueError("No commits found in PR")
        
        latest_commit = commits[-1]
        
        # Prepare review comments
        review_comments = []
        for comment in comments:
            review_comments.append({
                "path": comment.file_path,
                "line": comment.line_number,
                "body": comment.comment
            })
        
        # Create review with comments
        try:
            pr.create_review(
                commit=latest_commit,
                body="🤖 **Automated Code Review**\n\nI've analyzed the changes in this PR and found some areas for improvement. Please review the inline comments below.",
                event="COMMENT",
                comments=review_comments
            )
            return len(review_comments)
        except Exception as e:
            logger.error(f"Error creating review: {str(e)}")
            # Fallback: add individual comments
            added_comments = 0
            for comment in comments:
                try:
                    pr.create_issue_comment(f"**{comment.file_path}:{comment.line_number}**\n{comment.comment}")
                    added_comments += 1
                except Exception as e2:
                    logger.error(f"Error adding comment: {str(e2)}")
                    continue
            return added_comments 