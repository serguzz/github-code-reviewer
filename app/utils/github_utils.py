"""
GitHub utility functions
"""
import re
from typing import Dict, List, Any
from github.PullRequest import PullRequest

def parse_github_url(url: str) -> tuple[str, int]:
    """Parse GitHub PR URL to extract owner/repo and PR number"""
    # Expected format: https://github.com/owner/repo/pull/123
    pattern = r'https://github\.com/([^/]+)/([^/]+)/pull/(\d+)'
    match = re.match(pattern, url)
    
    if not match:
        raise ValueError(f"Invalid GitHub PR URL format: {url}")
    
    owner, repo, pr_number = match.groups()
    repo_name = f"{owner}/{repo}"
    return repo_name, int(pr_number)

def get_pr_files(pr: PullRequest) -> List[Dict[str, Any]]:
    """Get modified files from PR"""
    files = []
    for file in pr.get_files():
        if file.status in ['modified', 'added'] and file.patch:
            files.append({
                'filename': file.filename,
                'patch': file.patch,
                'additions': file.additions,
                'deletions': file.deletions
            })
    return files 