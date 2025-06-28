# GitHub PR Review Bot

An automated code review bot that analyzes GitHub pull requests and provides AI-powered feedback using OpenAI's GPT models.

## 🏗️ Project Structure

The application has been refactored into a clean modular architecture:

```
github_code_reviewer/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app initialization
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py           # App settings and environment variables
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   ├── database.py           # Database models and table schemas
│   │   └── schemas.py            # Pydantic models for API
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   ├── github_service.py     # GitHub API integration
│   │   ├── ai_service.py         # OpenAI integration
│   │   └── review_service.py     # Main review orchestration
│   ├── database/                 # Database operations
│   │   ├── __init__.py
│   │   └── operations.py         # Database CRUD operations
│   ├── api/                      # API routes
│   │   ├── __init__.py
│   │   └── routes.py             # FastAPI route definitions
│   ├── templates/                # HTML templates
│   │   └── index.html            # Main web interface template
│   ├── prompts/                  # AI prompt templates
│   │   ├── __init__.py
│   │   ├── prompt_loader.py      # Prompt loading utility
│   │   ├── code_review_prompt.txt # Main code review prompt
│   │   └── system_prompt.txt     # System role prompt
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── github_utils.py       # GitHub helper functions
├── requirements.txt              # Python dependencies
└── run.py                       # Application entry point
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token
- OpenAI API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd github_code_reviewer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   export GITHUB_TOKEN="your_github_token"
   export OPENAI_API_KEY="your_openai_api_key"
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

   The application will start on `http://localhost:8000`

## 📋 API Endpoints

- `GET /` - Web interface for submitting PR reviews
- `POST /review` - Submit a PR for review
- `GET /reviews` - Get recent review history
- `GET /health` - Health check endpoint

## 🧩 Architecture Overview

### Core Components

1. **Configuration (`app/config/`)**
   - Centralized settings management
   - Environment variable validation
   - Logging configuration

2. **Models (`app/models/`)**
   - `schemas.py`: Pydantic models for API requests/responses
   - `database.py`: Database models and table schemas

3. **Services (`app/services/`)**
   - `github_service.py`: GitHub API interactions
   - `ai_service.py`: OpenAI integration for code analysis
   - `review_service.py`: Main business logic orchestration

4. **Database (`app/database/`)**
   - SQLite operations for storing review data
   - Review and comment persistence

5. **API (`app/api/`)**
   - FastAPI route definitions
   - Request/response handling
   - Jinja2 template integration

6. **Templates (`app/templates/`)**
   - HTML templates for web interface
   - Clean separation of presentation and logic

7. **Prompts (`app/prompts/`)**
   - AI prompt templates for code review
   - Centralized prompt management
   - Easy prompt modification without code changes

8. **Utils (`app/utils/`)**
   - Helper functions for GitHub operations
   - URL parsing and validation

### Data Flow

1. User submits PR URL via web interface or API
2. `ReviewService` orchestrates the process:
   - `GitHubService` fetches PR data
   - `AIService` analyzes code changes
   - `GitHubService` posts review comments
   - `DatabaseOperations` stores results

## 🔧 Configuration

All configuration is centralized in `app/config/settings.py`:

- **AI Model**: Configure which OpenAI model to use
- **Database**: SQLite database file path
- **Logging**: Log file and format settings
- **Server**: Host and port configuration

## 🤖 Prompt Management

AI prompts are externalized to text files in `app/prompts/`:

- **`code_review_prompt.txt`**: Main prompt for code analysis
- **`system_prompt.txt`**: System role definition for the AI
- **`prompt_loader.py`**: Utility for loading and formatting prompts

**Benefits:**
- Modify prompts without touching code
- Version control for prompt changes
- Easy A/B testing of different prompt versions
- Clean separation of AI logic and prompt content

## 🗄️ Database Schema

The application uses SQLite with two main tables:

- **pr_reviews**: Stores PR review metadata
- **review_comments**: Stores individual review comments

## 🔒 Security

- Environment variables for sensitive data (tokens/keys)
- Input validation for GitHub URLs
- Error handling and logging

## 🧪 Development

The modular structure makes the codebase:
- **Maintainable**: Clear separation of concerns
- **Testable**: Each component can be tested independently
- **Extensible**: Easy to add new features or services
- **Scalable**: Services can be replaced or enhanced individually

## 📝 Migration from Legacy

This structure replaces the monolithic `main.py` file with:
- Better code organization
- Improved testability
- Cleaner dependency management
- Enhanced maintainability 