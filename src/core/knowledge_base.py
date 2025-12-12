#!/usr/bin/env python3
"""
Knowledge Base - Initial data for RAG system
Contains code patterns, best practices, and example projects.
"""

# Code Patterns
CODE_PATTERNS = [
    {
        "name": "User Authentication",
        "type": "authentication",
        "description": "Secure user authentication with JWT tokens and password hashing",
        "use_cases": [
            "User login/registration systems",
            "API authentication",
            "Session management"
        ],
        "code": """
# User Authentication Pattern
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

class UserAuth:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def hash_password(self, password):
        return generate_password_hash(password)
    
    def verify_password(self, password, hash):
        return check_password_hash(hash, password)
    
    def generate_token(self, user_id, expiry_hours=24):
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=expiry_hours)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
"""
    },
    {
        "name": "REST API Endpoint",
        "type": "api",
        "description": "Standard REST API endpoint with error handling and validation",
        "use_cases": [
            "Creating CRUD APIs",
            "Building microservices",
            "RESTful web services"
        ],
        "code": """
# REST API Endpoint Pattern
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

def validate_json(required_fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({"error": "Content-Type must be application/json"}), 400
            
            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return jsonify({
                    "error": "Missing required fields",
                    "fields": missing_fields
                }), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/api/resource', methods=['POST'])
@validate_json(['name', 'value'])
def create_resource():
    try:
        data = request.get_json()
        # Process data
        result = {"id": 123, "status": "created"}
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""
    },
    {
        "name": "Database Connection Pool",
        "type": "database",
        "description": "Efficient database connection pooling with context manager",
        "use_cases": [
            "Database applications",
            "Web applications with DB",
            "High-performance data access"
        ],
        "code": """
# Database Connection Pool Pattern
from contextlib import contextmanager
import psycopg2
from psycopg2 import pool

class DatabasePool:
    def __init__(self, minconn=1, maxconn=10, **kwargs):
        self.pool = psycopg2.pool.SimpleConnectionPool(
            minconn, maxconn, **kwargs
        )
    
    @contextmanager
    def get_connection(self):
        conn = self.pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)
    
    def execute_query(self, query, params=None):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
    
    def close_all(self):
        self.pool.closeall()
"""
    },
    {
        "name": "Async Task Queue",
        "type": "async",
        "description": "Asynchronous task queue for background processing",
        "use_cases": [
            "Background job processing",
            "Email sending",
            "Data processing pipelines"
        ],
        "code": """
# Async Task Queue Pattern
import asyncio
from typing import Callable, Any
from queue import Queue
from threading import Thread

class TaskQueue:
    def __init__(self, num_workers=4):
        self.queue = Queue()
        self.workers = []
        self.num_workers = num_workers
        self._start_workers()
    
    def _start_workers(self):
        for _ in range(self.num_workers):
            worker = Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def _worker(self):
        while True:
            task_func, args, kwargs = self.queue.get()
            try:
                task_func(*args, **kwargs)
            except Exception as e:
                print(f"Task error: {e}")
            finally:
                self.queue.task_done()
    
    def add_task(self, func: Callable, *args, **kwargs):
        self.queue.put((func, args, kwargs))
    
    def wait_completion(self):
        self.queue.join()
"""
    },
    {
        "name": "Rate Limiter",
        "type": "security",
        "description": "Rate limiting decorator to prevent API abuse",
        "use_cases": [
            "API rate limiting",
            "DDoS protection",
            "Resource usage control"
        ],
        "code": """
# Rate Limiter Pattern
from functools import wraps
from time import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_calls=100, time_window=60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = defaultdict(list)
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            key = self._get_key(*args, **kwargs)
            
            # Remove old calls outside time window
            self.calls[key] = [
                call_time for call_time in self.calls[key]
                if now - call_time < self.time_window
            ]
            
            # Check if limit exceeded
            if len(self.calls[key]) >= self.max_calls:
                raise Exception("Rate limit exceeded")
            
            # Add current call
            self.calls[key].append(now)
            
            return func(*args, **kwargs)
        return wrapper
    
    def _get_key(self, *args, **kwargs):
        # Override this to customize rate limiting key
        return "global"
"""
    }
]

# Best Practices
BEST_PRACTICES = [
    {
        "title": "Input Validation",
        "category": "security",
        "tags": ["security", "validation", "api"],
        "content": """
Always validate and sanitize user inputs:

1. Validate data types and formats
2. Check for required fields
3. Sanitize against SQL injection
4. Escape special characters
5. Use parameterized queries
6. Implement length limits
7. Validate against whitelist when possible

Example:
- Email: Use regex validation
- Passwords: Minimum 8 chars, require complexity
- IDs: Validate format and existence
- File uploads: Check file type and size

Never trust user input, even from authenticated users.
"""
    },
    {
        "title": "Error Handling",
        "category": "reliability",
        "tags": ["errors", "exceptions", "logging"],
        "content": """
Implement comprehensive error handling:

1. Use try-except blocks for risky operations
2. Log errors with context (timestamp, user, action)
3. Return user-friendly error messages
4. Don't expose sensitive info in errors
5. Implement retry logic for transient failures
6. Use dead letter queues for failed messages
7. Monitor error rates and alert on spikes

Error Response Format:
{
    "error": "Human-readable message",
    "error_code": "SPECIFIC_ERROR_CODE",
    "timestamp": "2024-01-01T12:00:00Z",
    "request_id": "uuid"
}

Never let exceptions crash the entire application.
"""
    },
    {
        "title": "Database Optimization",
        "category": "performance",
        "tags": ["database", "performance", "optimization"],
        "content": """
Optimize database queries and connections:

1. Use connection pooling (don't open/close per request)
2. Add indexes on frequently queried fields
3. Use prepared statements (prevents SQL injection too)
4. Implement pagination for large result sets
5. Cache frequently accessed data
6. Use read replicas for read-heavy workloads
7. Monitor slow queries and optimize them

Query Optimization:
- SELECT only needed columns (avoid SELECT *)
- Use LIMIT for large tables
- Use EXISTS instead of COUNT(*) for existence checks
- Avoid N+1 queries (use JOIN or batch loading)

Monitor query performance and set alerts for slow queries (>100ms).
"""
    },
    {
        "title": "API Design",
        "category": "architecture",
        "tags": ["api", "rest", "design"],
        "content": """
Follow RESTful API best practices:

1. Use proper HTTP methods (GET, POST, PUT, DELETE)
2. Use plural nouns for resources (/users not /user)
3. Use HTTP status codes correctly:
   - 200: Success
   - 201: Created
   - 400: Bad request (validation)
   - 401: Unauthorized
   - 403: Forbidden
   - 404: Not found
   - 500: Server error

4. Version your API (/api/v1/users)
5. Implement pagination for list endpoints
6. Use filtering and sorting query params
7. Return consistent JSON structure
8. Document with OpenAPI/Swagger
9. Implement rate limiting
10. Use API keys or OAuth for authentication

URL Structure:
- GET /api/v1/users - List users
- GET /api/v1/users/{id} - Get user
- POST /api/v1/users - Create user
- PUT /api/v1/users/{id} - Update user
- DELETE /api/v1/users/{id} - Delete user
"""
    },
    {
        "title": "Testing Strategy",
        "category": "quality",
        "tags": ["testing", "quality", "ci/cd"],
        "content": """
Implement comprehensive testing:

1. Unit Tests (70% coverage minimum)
   - Test individual functions/methods
   - Mock external dependencies
   - Fast execution (<1 second)

2. Integration Tests
   - Test component interactions
   - Use test database
   - Test API endpoints

3. End-to-End Tests
   - Test critical user flows
   - Use staging environment
   - Automated in CI/CD

4. Performance Tests
   - Load testing for scalability
   - Stress testing for limits
   - Monitor response times

5. Security Tests
   - Penetration testing
   - Dependency vulnerability scans
   - OWASP Top 10 checks

Testing Pyramid:
- Many unit tests (fast, cheap)
- Some integration tests (moderate)
- Few E2E tests (slow, expensive)

Run tests in CI/CD pipeline before deployment.
"""
    },
    {
        "title": "Logging and Monitoring",
        "category": "observability",
        "tags": ["logging", "monitoring", "devops"],
        "content": """
Implement comprehensive logging and monitoring:

1. Structured Logging:
   - Use JSON format for logs
   - Include timestamp, level, message
   - Add context (user_id, request_id, action)
   - Don't log sensitive data (passwords, tokens)

2. Log Levels:
   - ERROR: Critical issues requiring attention
   - WARN: Potential issues, recoverable
   - INFO: Important business events
   - DEBUG: Detailed diagnostic info (dev only)

3. Monitoring Metrics:
   - Request rate and latency
   - Error rate (4xx, 5xx)
   - Database query performance
   - Memory and CPU usage
   - Queue depths

4. Alerting:
   - Set alerts for critical metrics
   - Define SLAs (99.9% uptime, <200ms p95)
   - Use escalation policies
   - Include runbooks in alerts

5. Distributed Tracing:
   - Track requests across services
   - Measure end-to-end latency
   - Identify bottlenecks

Use tools like: ELK Stack, Prometheus, Grafana, Datadog, New Relic
"""
    },
    {
        "title": "Security Checklist",
        "category": "security",
        "tags": ["security", "checklist", "compliance"],
        "content": """
Security best practices checklist:

Authentication & Authorization:
☐ Use strong password hashing (bcrypt, argon2)
☐ Implement MFA for sensitive operations
☐ Use JWT or session tokens securely
☐ Implement proper RBAC (Role-Based Access Control)
☐ Expire tokens/sessions appropriately

Data Protection:
☐ Encrypt data at rest (database encryption)
☐ Encrypt data in transit (HTTPS/TLS)
☐ Never store passwords in plain text
☐ Don't log sensitive data
☐ Implement data retention policies

API Security:
☐ Validate all inputs
☐ Implement rate limiting
☐ Use API keys or OAuth
☐ Enable CORS properly
☐ Sanitize outputs (prevent XSS)

Infrastructure:
☐ Keep dependencies updated
☐ Scan for vulnerabilities regularly
☐ Use security headers (CSP, HSTS)
☐ Implement DDoS protection
☐ Regular security audits

Compliance:
☐ GDPR compliance (if EU users)
☐ HIPAA compliance (if health data)
☐ PCI DSS compliance (if payments)
☐ SOC 2 compliance (if enterprise)
"""
    }
]

# Example Past Projects
EXAMPLE_PROJECTS = [
    {
        "description": "Build REST API for e-commerce platform with user authentication, product catalog, and order processing",
        "tasks": [
            {"task": "Set up Flask application structure", "estimated_hours": 2},
            {"task": "Implement user authentication with JWT", "estimated_hours": 4},
            {"task": "Create product catalog endpoints (CRUD)", "estimated_hours": 3},
            {"task": "Implement shopping cart functionality", "estimated_hours": 4},
            {"task": "Create order processing system", "estimated_hours": 5},
            {"task": "Add payment integration (Stripe)", "estimated_hours": 6},
            {"task": "Implement inventory management", "estimated_hours": 4},
            {"task": "Add email notifications", "estimated_hours": 3},
            {"task": "Write unit and integration tests", "estimated_hours": 8},
            {"task": "Deploy to production with monitoring", "estimated_hours": 4}
        ],
        "outcome": "Success - API handles 1000+ requests/min, 99.9% uptime",
        "metadata": {
            "tech_stack": ["Flask", "PostgreSQL", "Redis", "Stripe"],
            "team_size": 3,
            "duration_weeks": 6
        }
    },
    {
        "description": "Implement microservices architecture for social media application with user profiles, posts, and messaging",
        "tasks": [
            {"task": "Design microservices architecture", "estimated_hours": 6},
            {"task": "Set up API Gateway (Kong)", "estimated_hours": 4},
            {"task": "Create User Service (authentication, profiles)", "estimated_hours": 8},
            {"task": "Create Post Service (CRUD, feed generation)", "estimated_hours": 8},
            {"task": "Create Messaging Service (real-time chat)", "estimated_hours": 10},
            {"task": "Implement service discovery (Consul)", "estimated_hours": 4},
            {"task": "Add inter-service communication (gRPC)", "estimated_hours": 6},
            {"task": "Set up message queue (RabbitMQ)", "estimated_hours": 4},
            {"task": "Implement distributed caching (Redis)", "estimated_hours": 3},
            {"task": "Add monitoring and logging (ELK stack)", "estimated_hours": 6},
            {"task": "Write integration tests", "estimated_hours": 8},
            {"task": "Deploy with Docker and Kubernetes", "estimated_hours": 8}
        ],
        "outcome": "Success - Handles 10,000+ concurrent users, scalable architecture",
        "metadata": {
            "tech_stack": ["Flask", "FastAPI", "PostgreSQL", "Redis", "RabbitMQ", "Kubernetes"],
            "team_size": 5,
            "duration_weeks": 10
        }
    },
    {
        "description": "Build data pipeline for real-time analytics with ETL, data warehouse, and visualization",
        "tasks": [
            {"task": "Design data pipeline architecture", "estimated_hours": 6},
            {"task": "Set up data ingestion (Apache Kafka)", "estimated_hours": 8},
            {"task": "Implement ETL processing (Apache Spark)", "estimated_hours": 10},
            {"task": "Create data warehouse (PostgreSQL/Redshift)", "estimated_hours": 6},
            {"task": "Build data quality checks", "estimated_hours": 4},
            {"task": "Implement incremental loading", "estimated_hours": 5},
            {"task": "Create analytics dashboards (Grafana)", "estimated_hours": 8},
            {"task": "Add alerting for data anomalies", "estimated_hours": 4},
            {"task": "Implement data retention policies", "estimated_hours": 3},
            {"task": "Write data pipeline tests", "estimated_hours": 6},
            {"task": "Deploy and monitor pipeline", "estimated_hours": 5}
        ],
        "outcome": "Success - Processes 1TB data/day with <5 minute latency",
        "metadata": {
            "tech_stack": ["Kafka", "Spark", "PostgreSQL", "Grafana", "Airflow"],
            "team_size": 4,
            "duration_weeks": 8
        }
    }
]

