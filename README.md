# Expense Tracker API

> A modern, RESTful API service for personal expense management built with FastAPI and PostgreSQL

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat-square&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?style=flat-square&logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

**Expense Tracker API** is a robust, production-ready backend service designed for tracking and managing personal expenses. Built with modern Python frameworks and best practices, it provides secure user authentication, comprehensive expense management capabilities, and RESTful endpoints for seamless integration with frontend applications.

The API is designed to be scalable, maintainable, and easy to deploy on cloud platforms such as Vercel, Heroku, or AWS.

### Key Use Cases

- Personal budget management
- Expense categorization and reporting
- Multi-user expense tracking
- Real-time expense monitoring
- Integration with mobile and web applications

## Features

### 🔐 Authentication & Security
- User registration and login with secure password hashing (Argon2)
- JWT (JSON Web Token) based authentication
- Configurable token expiration (default: 30 minutes)
- Password verification using industry-standard algorithms
- Protected endpoints with token validation

### 💰 Expense Management
- Create, read, update, and delete expenses
- Categorize expenses for better organization
- Add descriptions to track expense details
- Automatic timestamp tracking (creation dates)
- User-specific expense isolation (each user sees only their expenses)
- Pagination and filtering capabilities

### 🛡️ Data Integrity
- Relational database design with foreign keys
- ACID compliance through SQLAlchemy ORM
- Unique username constraints
- Input validation using Pydantic schemas
- Error handling with descriptive HTTP status codes

### 🌐 API Standards
- RESTful architecture following HTTP conventions
- CORS (Cross-Origin Resource Sharing) enabled
- Automatic OpenAPI/Swagger documentation
- JSON request/response format
- Comprehensive error messages

### 📚 Developer Experience
- Auto-generated API documentation at `/docs` (Swagger UI)
- Alternative documentation at `/redoc` (ReDoc)
- Clear endpoint descriptions and request/response examples
- Type hints throughout codebase for IDE support

## Tech Stack

### Backend Framework
- **FastAPI** (0.104.1) - Modern, fast web framework for building APIs with Python
  - Automatic API documentation generation
  - Built-in data validation using Pydantic
  - Dependency injection system
  - High performance (near equivalent to Node.js and Go)

### Database
- **PostgreSQL** - Reliable, open-source relational database
  - ACID compliance
  - Advanced query capabilities
  - Excellent for production environments
- **SQLAlchemy** (2.0.23) - Python ORM for database operations
  - Object-relational mapping
  - Query builder
  - Migration support ready

### Authentication & Security
- **python-jose** (3.3.0) - JWT token handling
- **cryptography** (41.0.7) - Cryptographic recipes and primitives
- **argon2-cffi** (23.1.0) - Password hashing algorithm
  - Memory-hard hash function
  - Resistant to GPU cracking attacks
  - Industry-recommended for password storage

### Data Validation
- **Pydantic** (2.5.0) - Data validation library
  - Runtime type checking
  - JSON serialization/deserialization
  - Schema validation

### Server & Deployment
- **Uvicorn** (0.24.0) - ASGI web server
  - Production-ready
  - Supports async/await
- **Vercel** configuration included for serverless deployment

### Development Dependencies
- **python-dotenv** (1.0.0) - Environment variable management
- **psycopg2-binary** (2.9.9) - PostgreSQL adapter for Python

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT APPLICATION                      │
│                       (Web Browser)                         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ HTTP/HTTPS
                  ↓
┌─────────────────────────────────────────────────────────────┐
│                   FASTAPI APPLICATION                       │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │  Auth Route  │ Expense Route│  Middleware (CORS, etc)  │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            Security Layer (JWT, Hashing)               │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          Pydantic Schemas (Data Validation)            │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ SQL
                  ↓
┌─────────────────────────────────────────────────────────────┐
│                  SQLALCHEMY ORM LAYER                       │
│              (Models: User, Expense)                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE                            │
│        ┌──────────────┬──────────────────┐                  │
│        │ users table  │ expenses table   │                  │
│        └──────────────┴──────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### Layered Architecture

- **Route Layer** - HTTP endpoints and request/response handling
- **Security Layer** - Authentication, authorization, password hashing
- **Schema Layer** - Data validation and transformation (Pydantic)
- **Model Layer** - Database table definitions and relationships
- **Database Layer** - Connection pooling, session management
- **Configuration Layer** - Environment variables and app settings

## Prerequisites

Before running this project, ensure you have:

- **Python 3.9+** installed
- **PostgreSQL 12+** database instance
- **pip** (Python package manager)
- **Git** for version control

### For Local Development
- Virtual environment (venv or conda)
- `.env` file with required environment variables

### For Deployment
- Vercel account (for serverless deployment)
- Environment variables configured in deployment platform

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shytyk-develop/finance-tracker-api
cd fast-api-n1
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Security
SECRET_KEY=your_secret_key_here

# Database
DATABASE_URL=postgresql://username:password@hostname:6543/database_name

# API Configuration (optional, has defaults)
API_TITLE=Expense Tracker API
API_DESCRIPTION=An API for tracking personal expenses
API_VERSION=1.0.0
```

### Database Connection String Format

```
postgresql://[user]:[password]@[hostname]:[port]/[database]
```

**Example with Supabase (PostgreSQL hosting service):**
```
postgresql://postgres:your_password@db.xxxxxxxxxxxx.supabase.co:6543/postgres
```

## Running the Application

### Development Mode

```bash
# Using run.py
python run.py

# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
# Using uvicorn without reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Initialize Database Tables

```bash
python init_db.py
```

This creates all database tables defined in the models.

## API Documentation

### Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all available endpoints
- Read detailed descriptions of each endpoint
- Test endpoints directly from the browser
- See request/response schemas
- Understand required parameters

## API Endpoints

### Authentication Endpoints

#### Register a New User

```http
POST /api/register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password_123"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "user_id": 1
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "User already exists"
}
```

---

#### Login (Obtain Access Token)

```http
POST /api/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password_123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### Expense Endpoints

All expense endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer {access_token}
```

#### Create Expense

```http
POST /api/create
Content-Type: application/json
Authorization: Bearer {token}

{
  "amount": 2500,
  "category": "Food",
  "description": "Lunch with team members"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "amount": 2500,
  "category": "Food",
  "description": "Lunch with team members",
  "created_at": "2026-01-21T10:30:00",
  "owner_id": 1
}
```

---

#### Get All User Expenses

```http
GET /api/expenses
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "amount": 2500,
    "category": "Food",
    "description": "Lunch with team members",
    "created_at": "2026-01-21T10:30:00",
    "owner_id": 1
  },
  {
    "id": 2,
    "amount": 5000,
    "category": "Transport",
    "description": "Taxi to office",
    "created_at": "2026-01-21T11:00:00",
    "owner_id": 1
  }
]
```

---

#### Update Expense

```http
PUT /api/expenses/{id}
Content-Type: application/json
Authorization: Bearer {token}

{
  "amount": 3000,
  "category": "Food",
  "description": "Updated lunch expense"
}
```

---

#### Delete Expense

```http
DELETE /api/expenses/{id}
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "message": "Expense deleted successfully"
}
```

---

## Usage Examples

### Complete Workflow

#### Step 1: Register a New User

```bash
curl -X POST "http://localhost:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "SecurePassword123!"
  }'
```

#### Step 2: Login to Get Access Token

```bash
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "SecurePassword123!"
  }'
```

Save the `access_token` from the response.

#### Step 3: Create an Expense

```bash
curl -X POST "http://localhost:8000/api/create" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1500,
    "category": "Groceries",
    "description": "Weekly shopping"
  }'
```

#### Step 4: Retrieve All Expenses

```bash
curl -X GET "http://localhost:8000/api/expenses" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Step 5: Update an Expense

```bash
curl -X PUT "http://localhost:8000/api/expenses/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1600,
    "category": "Groceries",
    "description": "Weekly shopping - updated price"
  }'
```

#### Step 6: Delete an Expense

```bash
curl -X DELETE "http://localhost:8000/api/expenses/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure

```
fast-api-n1/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application setup
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration and environment variables
│   │   └── security.py            # Authentication and password hashing
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py            # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # User database model
│   │   └── expense.py             # Expense database model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                # Authentication endpoints
│   │   └── expenses.py            # Expense management endpoints
│   └── schemas/
│       ├── __init__.py
│       ├── user.py                # User data validation schemas
│       └── expense.py             # Expense data validation schemas
├── api.py                         # Alternative entry point
├── run.py                         # Development server runner
├── init_db.py                     # Database initialization script
├── requirements.txt               # Python dependencies
├── vercel.json                    # Vercel deployment configuration
└── README.md                      # This file
```


## Database Schema

### Users Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique user identifier |
| username | String | UNIQUE, NOT NULL | User's login name |
| hashed_password | String | NOT NULL | Argon2 hashed password |
| created_at | DateTime | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

### Expenses Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique expense identifier |
| amount | Integer | NOT NULL | Expense amount (in cents) |
| category | String | NOT NULL | Expense category |
| description | String | NULLABLE | Optional expense details |
| created_at | DateTime | DEFAULT CURRENT_TIMESTAMP | Expense creation timestamp |
| owner_id | Integer | FOREIGN KEY (users.id) | Reference to expense owner |

## Error Handling

The API implements comprehensive error handling with meaningful HTTP status codes and messages:

| Status Code | Meaning | Example |
|-------------|---------|---------|
| 200 | OK | Successful GET, PUT, DELETE request |
| 201 | Created | Successful resource creation |
| 400 | Bad Request | Invalid input, validation failed |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | User attempting unauthorized action |
| 404 | Not Found | Resource does not exist |
| 500 | Internal Server Error | Server-side error |

## Security Considerations

1. **Password Security**
   - Passwords are hashed using Argon2 algorithm
   - Never stored in plain text
   - Uses salt to prevent rainbow table attacks

2. **Token Management**
   - JWT tokens expire after 30 minutes
   - Tokens are signed with a secret key
   - Only the server can create and validate tokens

3. **Data Isolation**
   - Users only see their own expenses
   - Database enforces foreign key relationships
   - API enforces authorization checks

4. **Production Recommendations**
   - Use HTTPS/TLS for all communications
   - Rotate SECRET_KEY regularly
   - Store environment variables securely
   - Use environment-specific configurations
   - Enable rate limiting for API endpoints
   - Implement request logging and monitoring
   - Use a Web Application Firewall (WAF)

## Deployment

### Vercel (Recommended for Serverless)

1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Set environment variables in Vercel dashboard:
   - `SECRET_KEY`
   - `DATABASE_URL`
4. Deploy with `vercel deploy`

For detailed Vercel configuration, see `vercel.json`.

### Traditional Hosting (AWS, Heroku, DigitalOcean)

1. Ensure PostgreSQL is running and accessible
2. Set environment variables on the hosting platform
3. Run: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Development Workflow

### Adding a New Endpoint

1. Create a schema in `app/schemas/` (Pydantic model)
2. Create or update a model in `app/models/` (SQLAlchemy model)
3. Add the route handler in `app/routes/`
4. Import and include the router in `app/main.py`
5. Test using `/docs` endpoint

### Best Practices

- Always validate input using Pydantic schemas
- Use type hints for better IDE support and documentation
- Follow RESTful conventions for endpoint naming
- Keep business logic in route handlers or separate service files
- Write meaningful error messages for debugging

## Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and commit: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Standards

- Follow PEP 8 Python style guide
- Add type hints to all functions
- Document complex logic with comments
- Test your changes before submitting PR

## Troubleshooting

### Database Connection Issues

```
Error: could not translate host name "db.xxx.supabase.co" to address
```
- Check your DATABASE_URL in `.env`
- Verify PostgreSQL is running and accessible
- Check firewall and network settings

### Token Expired

```
Error: "Could not validate credentials"
```
- Obtain a new token by logging in again
- Check token expiration time in config (default: 30 minutes)

### Port Already in Use

```
Error: Address already in use
```
- Change port: `uvicorn app.main:app --port 8001`
- Or kill the process using port 8000

## Performance & Scalability

- **Connection Pooling**: SQLAlchemy manages database connection pool
- **Async Support**: FastAPI supports async endpoints for high concurrency
- **Caching Ready**: Architecture supports Redis caching integration
- **Horizontal Scaling**: Stateless design allows running multiple instances
- **Load Balancing**: Compatible with any load balancer (nginx, HAProxy, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation

## Author

**Yan Shytyk**


---

**Last Updated:** January 22, 2026  
**API Version:** 1.0.0  
**Status:** Active Development
