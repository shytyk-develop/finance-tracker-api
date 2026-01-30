# Finance Tracker API

A FastAPI-based application for personal financial management. Track income and expenses, calculate balances, and manage transactions with JWT authentication and PostgreSQL.

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [API Endpoints](#-api-endpoints)
- [Usage Examples](#-usage-examples)
- [Database Schema](#-database-schema)
- [Security](#-security)
- [Rate Limiting](#-rate-limiting)
- [Error Handling](#-error-handling)
- [Testing](#-testing)
- [Deployment](#-deployment)


## 🌟 Overview

The Finance Tracker API is a robust, secure FastAPI application designed for personal financial management. It allows users to track income and expenses, calculate real-time balances, and perform advanced queries on transactions. Built with modern Python tools and PostgreSQL, it ensures data security through JWT authentication and user isolation.

Key benefits:
- **Easy Tracking**: Log income and expenses with categories and descriptions.
- **Smart Calculations**: Automatic balance computation using database aggregations.
- **Flexible Queries**: Filter transactions by date, amount, category, or type.
- **Secure Access**: JWT tokens for authentication, with rate limiting to prevent abuse.
- **Developer-Friendly**: Auto-generated OpenAPI docs and comprehensive error handling.

## 🚀 Features

- **Authentication**:
  - JWT-based authentication with bearer tokens
  - User registration and secure login/logout
  - Password hashing with Argon2

- **Transaction Management**:
  - CRUD operations for income/expense transactions
  - Support for categories, descriptions, and amounts
  - Validation to ensure positive amounts and valid data

- **Balance & Analytics**:
  - Real-time balance calculation using SQL aggregations
  - Separate totals for income and expenses

- **Querying & Filtering**:
  - Advanced filtering by category, type, date range, and amount range
  - Pagination for large datasets
  - Sorting and offset support

- **Security & Performance**:
  - Rate limiting to prevent abuse (3-5 req/min)
  - Pydantic validation for all inputs
  - Data isolation per user
  - Auto-generated API docs at `/docs` and `/redoc`

## 🛠 Tech Stack

| Component          | Technology                  | Purpose                          |
|--------------------|-----------------------------|----------------------------------|
| **Backend**       | FastAPI 0.104.1            | High-performance web framework with async support |
| **ORM**           | SQLAlchemy 2.0.23          | Database abstraction and query building |
| **Database**      | PostgreSQL 13+             | Relational database with ACID compliance |
| **Authentication**| python-jose 3.3.0          | JWT token creation and validation |
| **Password Hashing**| argon2-cffi 23.1.0       | Secure password hashing |
| **Validation**    | Pydantic 2.5.0             | Data validation and serialization |
| **Rate Limiting** | SlowAPI 0.1.9              | API rate limiting with Redis support |
| **Server**        | Uvicorn 0.24.0             | ASGI server for production deployment |

## 🏗 Architecture

The application follows a layered architecture for maintainability:

```
finance-tracker-api/
├── app/
│   ├── core/               # Core utilities
│   │   ├── config.py       # App settings and env vars
│   │   ├── security.py     # JWT and password functions
│   │   └── limiter.py      # Rate limiting config
│   ├── db/                 # Database layer
│   │   └── database.py     # SQLAlchemy engine and session
│   ├── models/             # Data models
│   │   ├── user.py         # UserDB model
│   │   └── expense.py      # TransactionDB model
│   ├── routes/             # API endpoints
│   │   ├── auth.py         # Auth routes
│   │   └── transactions.py # Transaction CRUD
│   ├── schemas/            # Pydantic models
│   │   ├── user.py         # Auth schemas
│   │   └── expense.py      # Transaction schemas
│   └── main.py             # FastAPI app setup
├── requirements.txt
├── run.py
├── init_db.py
└── README.md
```

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
│              (Models: User, Transaction)                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE                            │
│        ┌──────────────┬────────────────────┐                │
│        │ users table  │ transactions table │                │
│        └──────────────┴────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### Key Components
- **Core Layer**: Handles configuration, security, and utilities.
- **DB Layer**: Manages database connections and sessions.
- **Models Layer**: Defines SQLAlchemy tables.
- **Routes Layer**: Contains API endpoints with business logic.
- **Schemas Layer**: Validates input/output data.

## 📦 Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 13+ or Supabase

### Setup
1. Clone and enter directory
2. Create venv: `python -m venv venv && source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Create `.env`:
   ```
   SECRET_KEY=your-32-char-key
   DATABASE_URL=postgresql://user:pass@host/db
   ```
5. Init DB: `python init_db.py`
6. Run: `python run.py`

Access at http://127.0.0.1:8000/docs

## ⚙ Configuration

Key environment variables:
- `SECRET_KEY`: JWT key (32+ chars)
- `DATABASE_URL`: PostgreSQL connection
- `REDIS_URL`: Optional for rate limiting

## 📡 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/login` | Login | No |
| POST | `/api/auth/logout` | Logout | Yes |
| POST | `/api/create_expense` | Create expense | Yes |
| POST | `/api/create_income` | Create income | Yes |
| GET | `/api/get` | List transactions (with filters) | Yes |
| PUT | `/api/update/{id}` | Update transaction | Yes |
| DELETE | `/api/delete/{id}` | Delete transaction | Yes |
| GET | `/api/get_balance` | Get balance | Yes |

## 💡 Usage Examples

### Register
```bash
curl -X POST "http://127.0.0.1:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "password": "securepass123"}'
# Response: {"message": "User created successfully", "user_id": 1}
```

### Login
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=user&password=pass'
# Response: {"access_token": "eyJ...", "token_type": "bearer"}
```

### Create Income
```bash
curl -X POST "http://127.0.0.1:8000/api/create_income" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 5000, "category": "Salary", "description": "Monthly pay"}'
```

### Update Transaction
```bash
curl -X PUT "http://127.0.0.1:8000/api/update/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1200, "category": "Food"}'
```

### Delete Transaction
```bash
curl -X DELETE "http://127.0.0.1:8000/api/delete/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
# Response: {"message": "Transaction deleted"}
```

### Python Client
```python
import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "your_jwt_token"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Create expense
response = requests.post(f"{BASE_URL}/api/create_expense", 
                         json={"amount": 100, "category": "Misc"}, 
                         headers=headers)
print(response.json())

# Get balance
balance = requests.get(f"{BASE_URL}/api/get_balance", headers=headers).json()
print(f"Balance: {balance['current_balance']}")
```

## 🗄 Database Schema

### Tables

#### users
| Column          | Type          | Constraints              | Description |
|-----------------|---------------|--------------------------|-------------|
| id             | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Unique user ID |
| username       | VARCHAR      | UNIQUE, NOT NULL        | User login name |
| hashed_password| VARCHAR      | NOT NULL                | Argon2 hashed password |
| created_at     | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP| Account creation time |

#### transactions
| Column      | Type          | Constraints              | Description |
|-------------|---------------|--------------------------|-------------|
| id         | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Unique transaction ID |
| amount     | INTEGER      | NOT NULL, CHECK > 0     | Transaction amount (cents) |
| category   | VARCHAR      | NOT NULL, MAX 40 chars  | Category (e.g., "Food") |
| description| VARCHAR      | NULL, MAX 100 chars     | Optional description |
| type       | ENUM         | NOT NULL, DEFAULT 'expense' | 'income' or 'expense' |
| created_at | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP| Transaction timestamp |
| owner_id   | INTEGER      | FOREIGN KEY → users.id  | Owner user ID |

### Relationships
- One-to-Many: users → transactions

### Sample Data
```sql
INSERT INTO users (username, hashed_password) VALUES ('user1', 'hashed_pass');
INSERT INTO transactions (amount, category, type, owner_id) VALUES
(5000, 'Salary', 'income', 1),
(1000, 'Groceries', 'expense', 1);
```

## 🔒 Security

- JWT tokens for authentication
- Argon2 password hashing
- Input validation with Pydantic
- Data isolation by user ID

## 🛡️ Rate Limiting

Limits applied per endpoint:
- Auth endpoints: 3/min
- Create transactions: 5/min
- Other endpoints: 10/min

## 🚨 Error Handling

Common status codes:
- 200: Success
- 401: Unauthorized
- 404: Not found
- 422: Validation error
- 429: Rate limit exceeded
- 500: Internal error

## 🧪 Testing

Run tests with `pytest`.

### Example Test
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_transaction():
    # Assume login first
    response = client.post("/api/create_expense", 
                           json={"amount": 100, "category": "Test"},
                           headers={"Authorization": "Bearer token"})
    assert response.status_code == 200
```

Install pytest: `pip install pytest`

## 🚀 Deployment

### Local
`python run.py`

### Production
Use Gunicorn/Uvicorn or Docker. Set env vars for secrets.

### Supabase
Use Supabase PostgreSQL URL in `DATABASE_URL`.

## Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes
4. Run tests
5. Submit a PR

## Changelog

### v1.0.0
- Initial release with basic features

## Troubleshooting

- **DB Connection**: Check `DATABASE_URL` and PostgreSQL status
- **401 Unauthorized**: Verify JWT token in Authorization header
- **429 Rate Limit**: Wait or check limits
- **422 Validation**: Check input format
- **Registration fails**: Username might be taken

Enable `DEBUG=True` for logs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Yan Shytyk**


---

**Last Updated:** January 30, 2026  
**API Version:** 1.0.0  