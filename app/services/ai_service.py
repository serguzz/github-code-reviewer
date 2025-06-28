"""
AI service for code analysis using OpenAI
"""
import json
import logging
from typing import List, Dict, Any
import openai

from ..config.settings import OPENAI_API_KEY, MODEL
from ..models.database import ReviewComment
from ..prompts.prompt_loader import prompt_loader

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI-powered code analysis"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        openai.api_key = OPENAI_API_KEY
    
    def analyze_code_with_ai(self, files: List[Dict[str, Any]], pr_title: str, pr_body: str) -> List[ReviewComment]:
        """Analyze code changes using OpenAI"""
        comments = []
        
        for file_info in files:
            filename = file_info['filename']
            patch = file_info['patch']
            
            # Skip very large files
            if len(patch) > 10000:
                logger.warning(f"Skipping large file: {filename}")
                continue
            
            file_comments = self._analyze_single_file(filename, patch, pr_title, pr_body)
            comments.extend(file_comments)
        
        return comments
    
    def _analyze_single_file(self, filename: str, patch: str, pr_title: str, pr_body: str) -> List[ReviewComment]:
        """Analyze a single file with AI"""
        # Load and format AI prompt from template
        prompt = prompt_loader.format_prompt(
            "code_review_prompt",
            pr_title=pr_title,
            pr_body=pr_body,
            filename=filename,
            patch=patch
        )

        try:
            # Load system prompt from file
            system_prompt = prompt_loader.load_prompt("system_prompt")
            
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse AI response
            ai_response = response.choices[0].message.content
            
            # Extract JSON from response
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = ai_response[json_start:json_end]
                result = json.loads(json_str)
                
                comments = []
                for comment_data in result.get('comments', []):
                    if comment_data.get('line_number') and comment_data.get('comment'):
                        comments.append(ReviewComment(
                            file_path=filename,
                            line_number=comment_data['line_number'],
                            comment=comment_data['comment']
                        ))
                return comments
            
        except Exception as e:
            logger.error(f"Error analyzing file {filename}: {str(e)}")
        
        return [] 