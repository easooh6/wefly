**✈️ WeFly - AI-Powered Flight Booking Platform**

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Redis](https://img.shields.io/badge/Redis-7-red.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-70%25-yellowgreen.svg)

🎯 Project Features
🚀 Unique Capabilities:
🎤 AI Voice Search - ticket search via voice commands (Google Gemini)

🔄 Asynchronous Parsing - high-performance data collection from airline APIs

🔐 Full Authentication - JWT + Refresh tokens, email verification

📊 Real-time Data - up-to-date flight information

🧪 Comprehensive Testing - 70%+ code coverage

🏗️ Architecture:
✅ Clean Architecture - separation into domain/infrastructure/presentation

✅ DDD Approach - Domain-Driven Design

✅ SOLID Principles - maintainable and extensible code

✅ Dependency Injection - weak component coupling

**🛠️ Technology Stack**
Backend:
Python 3.12 - modern language version

FastAPI - high-performance async web framework

SQLAlchemy 2.0 - async ORM for database operations

Pydantic - data validation and type safety

Celery - background tasks and email distribution

Databases:
PostgreSQL 15 - primary relational database

Redis 7 - caching, rate limiting, task queues

Alembic - database migrations

AI/ML:
Google Gemini API - processing voice commands

Audio processing - handling audio files

DevOps:
Docker + Docker Compose - containerization

GitLab CI/CD - automated testing and deployment

Uvicorn - ASGI server with uvloop

Testing:
Pytest - testing framework

pytest-asyncio - testing async code

pytest-cov - code coverage reporting

httpx - async HTTP client for API tests

🚀 Quick Start
Prerequisites:
Docker and Docker Compose

Python 3.12+ (for local development)

Git

1️⃣ Clone the Repository:
Bash

git clone https://github.com/yourusername/wefly.git
cd wefly/app
2️⃣ Configure Environment Variables:
Bash

cp .env.example .env
Edit the .env file:

# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=wefly
POSTGRES_USER=wefly_user
POSTGRES_PASSWORD=secure_password_here

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# AI
GEMINI_API_KEY=your-gemini-api-key
3️⃣ Run with Docker:
Bash

# Build and run all services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
4️⃣ Apply Migrations:
Bash

docker-compose exec api alembic upgrade head
5️⃣ Check Functionality:
Open in your browser:

API Documentation: http://localhost:8000/docs

Health Check: http://localhost:8000/health

🧪 Testing
Run All Tests:
Bash

# Inside Docker container
docker-compose exec api pytest tests/ -v

# Locally
pytest tests/ -v
Run by Test Type:
Bash

# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Presentation tests
pytest tests/presentation/ -v
Code Coverage:
Bash

# With coverage report
pytest tests/ --cov=src --cov-report=html

# View HTML report
open htmlcov/index.html
Run Specific Test:
Bash

pytest tests/unit/domain/auth/test_register.py::test_register_user_success -v
📡 API Endpoints
Authentication (/auth):
POST /auth/send-verification
Send verification code to email

JSON

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure_password123"
}
POST /auth/registration
Register a new user

JSON

{
  "email": "john@example.com",
  "code": 123456
}
POST /auth/login
User authentication

JSON

{
  "email": "john@example.com",
  "password": "secure_password123"
}
Response:

JSON

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
POST /auth/refresh
Refresh access token

JSON

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
POST /auth/logout
Log out of the system

JSON

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
User (/user):
GET /user/tickets
Retrieve user's tickets (requires authorization)

Bash

curl -H "Authorization: Bearer <access_token>" http://localhost:8000/user/tickets
POST /user/add_ticket
Add a ticket to favorites (requires authorization)

JSON

{
  "id": "flight-123",
  "name": "Moscow - New York",
  "racenumber": "SU100",
  "departuredate": "2025-06-30",
  "departuretime": "10:00",
  "originport": "SVO",
  "origincityName": "Moscow",
  "arrivaldate": "2025-06-30",
  "arrivaltime": "14:00",
  "destinationport": "JFK",
  "destinationcityName": "New York",
  "flighttime": "10h",
  "price_light": 30000,
  "price_optimal": 45000,
  "price_comfort": 60000
}
Search (/search):
POST /search/search
One-way ticket search

JSON

{
  "date[0]": "30.12.2025",
  "originport": "SVO",
  "destinationport": "JFK"
}
POST /search/search_round
Round-trip ticket search

JSON

{
  "date[0]": "30.12.2025",
  "date[1]": "10.01.2026",
  "originport": "SVO",
  "destinationport": "JFK"
}
POST /search/search_voice
🎤 AI Voice Search (unique feature!)

Bash

curl -X POST http://localhost:8000/search/search_voice \
  -H "Authorization: Bearer <access_token>" \
  -F "audio=@voice_command.mp3"
Example Voice Command:

"Find me tickets from Moscow to New York for December 30th"

🔐 Security
Implemented Measures:
✅ JWT Authentication with access and refresh tokens

✅ Bcrypt Hashing for passwords

✅ Email Verification upon registration

✅ Rate Limiting (3 requests/minute for registration)

✅ CORS Configuration

✅ Input Data Validation via Pydantic

✅ SQL Injection Protection via ORM

Environment Variables:
All sensitive data is stored in the .env file and is not committed to the repository.

📊 Monitoring and Logging
Logs:
Bash

# View API logs
docker-compose logs -f api

# View Celery worker logs
docker-compose logs -f celery_worker

# View PostgreSQL logs
docker-compose logs -f postgres
Health Checks:
API: GET /health

Database: automated health checks in Docker

Redis: automated health checks in Docker

🔄 CI/CD Pipeline
GitLab CI Stages:
Build - building Docker images

Test - running unit/integration/presentation tests

Security - security scanning

Deploy - deployment to staging/production

Automation:
✅ Tests run on every push

✅ Coverage reports are automatically generated

✅ Security scans for dependencies

✅ Automated cleanup after tests
