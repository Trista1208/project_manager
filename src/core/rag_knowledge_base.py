#!/usr/bin/env python3
"""
Initial Knowledge Base for RAG System
Populates the RAG system with DevOps best practices, code patterns, and common solutions.
"""

from .rag_system import RAGSystem


def populate_initial_knowledge(rag: RAGSystem):
    """Populate RAG system with initial DevOps knowledge."""
    
    print("📚 Populating initial knowledge base...")
    
    # ===== BEST PRACTICES =====
    print("  Adding best practices...")
    
    rag.store_best_practice(
        "Use Environment Variables for Configuration",
        """Always use environment variables for configuration and secrets.
        - Never hardcode API keys, passwords, or sensitive data
        - Use .env files for local development
        - Use secret management services (AWS Secrets Manager, etc.) for production
        - Validate required environment variables at startup""",
        category="security"
    )
    
    rag.store_best_practice(
        "Implement Comprehensive Error Handling",
        """All API calls and external operations should have error handling.
        - Use try-except blocks for external API calls
        - Log errors with context (what operation failed, why)
        - Provide meaningful error messages to users
        - Implement retry logic for transient failures
        - Use circuit breakers for failing services""",
        category="reliability"
    )
    
    rag.store_best_practice(
        "Write Tests for All Critical Paths",
        """Test coverage should include:
        - Unit tests for business logic
        - Integration tests for API endpoints
        - End-to-end tests for critical workflows
        - Mock external dependencies
        - Test error conditions, not just happy paths""",
        category="testing"
    )
    
    rag.store_best_practice(
        "Use Semantic Versioning",
        """Follow semantic versioning (MAJOR.MINOR.PATCH):
        - MAJOR: Breaking changes
        - MINOR: New features (backward compatible)
        - PATCH: Bug fixes
        - Tag releases in git
        - Maintain CHANGELOG.md""",
        category="versioning"
    )
    
    rag.store_best_practice(
        "Implement Proper Logging",
        """Structured logging best practices:
        - Use different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        - Include context (timestamp, user, operation, trace ID)
        - Log at critical decision points
        - Don't log sensitive data (passwords, tokens)
        - Use structured logging (JSON format) for easier parsing""",
        category="observability"
    )
    
    rag.store_best_practice(
        "API Design Best Practices",
        """RESTful API best practices:
        - Use proper HTTP methods (GET, POST, PUT, DELETE)
        - Return appropriate status codes (200, 201, 400, 404, 500)
        - Use consistent naming conventions (plural nouns, kebab-case)
        - Version your API (/v1/, /v2/)
        - Document with OpenAPI/Swagger
        - Implement rate limiting
        - Use authentication and authorization""",
        category="api_design"
    )
    
    rag.store_best_practice(
        "Database Best Practices",
        """Database design and usage:
        - Use migrations for schema changes
        - Index frequently queried columns
        - Use connection pooling
        - Implement database backups
        - Never store passwords in plain text (use bcrypt, argon2)
        - Use transactions for atomic operations
        - Implement soft deletes for important data""",
        category="database"
    )
    
    rag.store_best_practice(
        "CI/CD Pipeline Essentials",
        """Continuous Integration/Deployment:
        - Run tests on every commit
        - Use automated code quality checks (linters, formatters)
        - Build Docker images for consistency
        - Deploy to staging before production
        - Implement automated rollback on failure
        - Use blue-green or canary deployments
        - Monitor deployments and set up alerts""",
        category="cicd"
    )
    
    # ===== CODE PATTERNS =====
    print("  Adding code patterns...")
    
    rag.store_code_pattern(
        "API Client with Retry Logic",
        """
import requests
from time import sleep

def api_call_with_retry(url, max_retries=3, backoff=2):
    \"\"\"Make API call with exponential backoff retry.\"\"\"
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait_time = backoff ** attempt
            print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
            sleep(wait_time)
""",
        "Use for external API calls to handle transient failures",
        language="python",
        use_cases=[
            "GitHub API calls",
            "Jira API calls",
            "Any external HTTP API",
            "Slack notifications"
        ]
    )
    
    rag.store_code_pattern(
        "Environment Configuration Loader",
        """
import os
from dotenv import load_dotenv

class Config:
    \"\"\"Configuration from environment variables.\"\"\"
    
    def __init__(self):
        load_dotenv()
        
        # Required
        self.api_key = self._get_required('API_KEY')
        self.github_token = self._get_required('GITHUB_TOKEN')
        
        # Optional
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    def _get_required(self, key):
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} not set")
        return value
""",
        "Safe configuration loading with validation",
        language="python",
        use_cases=[
            "Application startup",
            "Loading API credentials",
            "Configuration management"
        ]
    )
    
    rag.store_code_pattern(
        "Structured Error Response",
        """
from flask import jsonify

def error_response(message, status_code=400, details=None):
    \"\"\"Return structured error response.\"\"\"
    response = {
        'success': False,
        'error': {
            'message': message,
            'code': status_code
        }
    }
    if details:
        response['error']['details'] = details
    
    return jsonify(response), status_code

# Usage:
# return error_response("Invalid input", 400, {"field": "email"})
""",
        "Consistent error responses for APIs",
        language="python",
        use_cases=[
            "REST API error handling",
            "Input validation errors",
            "Authentication failures"
        ]
    )
    
    # ===== COMMON TASKS =====
    print("  Adding common task patterns...")
    
    rag.store_task(
        "Implement user authentication with JWT",
        """Successfully implemented JWT-based authentication:
        1. Created login endpoint that validates credentials
        2. Generated JWT tokens with user ID and expiration
        3. Implemented middleware to verify tokens on protected routes
        4. Added refresh token mechanism
        5. Stored hashed passwords using bcrypt
        Time: ~6 hours
        Cost: $0.00 (used local models)""",
        metadata={
            "type": "authentication",
            "complexity": "medium",
            "duration_hours": 6,
            "technologies": "JWT, bcrypt, Flask"
        }
    )
    
    rag.store_task(
        "Set up CI/CD pipeline with GitHub Actions",
        """Successfully set up automated CI/CD:
        1. Created .github/workflows/ci.yml
        2. Added tests, linting, and formatting checks
        3. Configured Docker image building
        4. Set up automated deployment to staging
        5. Added environment-based configurations
        Time: ~4 hours
        Cost: $0.00 (GitHub Actions free tier)""",
        metadata={
            "type": "cicd",
            "complexity": "medium",
            "duration_hours": 4,
            "technologies": "GitHub Actions, Docker, pytest"
        }
    )
    
    rag.store_task(
        "Integrate third-party API (Stripe payments)",
        """Successfully integrated payment processing:
        1. Set up Stripe SDK and API keys
        2. Implemented payment intent creation
        3. Added webhook handling for payment events
        4. Implemented error handling and retry logic
        5. Added comprehensive logging
        Time: ~8 hours
        Cost: $0.00 (Stripe test mode)""",
        metadata={
            "type": "integration",
            "complexity": "high",
            "duration_hours": 8,
            "technologies": "Stripe, webhooks, async"
        }
    )
    
    # ===== ERROR RESOLUTIONS =====
    print("  Adding error solutions...")
    
    rag.store_error_resolution(
        "ModuleNotFoundError: No module named 'xyz'",
        """Solution:
        1. Check if package is in requirements.txt
        2. Run: pip install -r requirements.txt
        3. If using virtual env, make sure it's activated
        4. Verify Python version compatibility
        5. Clear pip cache if needed: pip cache purge""",
        context="Common when dependencies are not installed or wrong Python environment is used"
    )
    
    rag.store_error_resolution(
        "401 Unauthorized API Error",
        """Solution:
        1. Verify API key/token is correct
        2. Check if token has expired
        3. Ensure token has required permissions/scopes
        4. Verify authentication header format (Bearer, Basic, etc.)
        5. Check if API endpoint requires different auth method""",
        context="Common with third-party API integrations (GitHub, Jira, Slack)"
    )
    
    rag.store_error_resolution(
        "Rate limit exceeded (429 Too Many Requests)",
        """Solution:
        1. Implement exponential backoff retry
        2. Add rate limiting to your client
        3. Cache responses when possible
        4. Use pagination for large datasets
        5. Request higher rate limits from provider if needed
        6. Consider implementing a queue system""",
        context="Common with high-volume API usage"
    )
    
    rag.store_error_resolution(
        "Database connection timeout",
        """Solution:
        1. Check database is running and accessible
        2. Verify connection string and credentials
        3. Check network connectivity and firewall rules
        4. Increase connection timeout setting
        5. Implement connection pooling
        6. Add connection retry logic with backoff""",
        context="Common in production when database is under load"
    )
    
    print("✅ Initial knowledge base populated!")
    
    # Print statistics
    stats = rag.get_statistics()
    print(f"\n📊 Knowledge Base Statistics:")
    print(f"   Total documents: {stats['total_documents']}")
    for collection, count in stats.items():
        if collection not in ['total_documents', 'collections']:
            print(f"   - {collection}: {count}")


if __name__ == "__main__":
    print("🚀 Initializing RAG Knowledge Base...")
    
    rag = RAGSystem()
    populate_initial_knowledge(rag)
    
    print("\n🧪 Testing retrieval...")
    
    # Test retrieval
    results = rag.retrieve_best_practices("API security", k=2)
    print(f"\n📚 Best practices for 'API security':")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['metadata']['title']}")
    
    results = rag.retrieve_similar_tasks("add user login", k=2)
    print(f"\n📋 Similar tasks to 'add user login':")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['metadata']['description']}")
    
    print("\n✅ Knowledge base ready for use!")

