"""
Utility for loading and formatting prompt templates
"""
import os
from pathlib import Path
from typing import Dict, Any

class PromptLoader:
    """Load and format prompt templates from files"""
    
    def __init__(self):
        """Initialize with prompts directory path"""
        self.prompts_dir = Path(__file__).parent
    
    def load_prompt(self, prompt_name: str) -> str:
        """Load a prompt template from file"""
        prompt_file = self.prompts_dir / f"{prompt_name}.txt"
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def format_prompt(self, prompt_name: str, **kwargs) -> str:
        """Load and format a prompt template with variables"""
        template = self.load_prompt(prompt_name)
        
        # Handle None values by replacing with default text
        formatted_kwargs = {}
        for key, value in kwargs.items():
            if value is None:
                if key == 'pr_body':
                    formatted_kwargs[key] = 'No description provided'
                else:
                    formatted_kwargs[key] = ''
            else:
                formatted_kwargs[key] = value
        
        return template.format(**formatted_kwargs)

# Global instance for easy importing
prompt_loader = PromptLoader() 