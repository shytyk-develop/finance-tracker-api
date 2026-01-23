# Copilot Instructions for Expense Tracker API

## Architecture Overview

**Expense Tracker API** is a FastAPI application for personal expense management with JWT authentication and PostgreSQL persistence. The architecture follows a layered pattern:

- **Routes** (`app/routes/`): HTTP endpoints with dependency injection
- **Models** (`app/models/`): SQLAlchemy ORM table definitions (UserDB, ExpenseDB)
- **Schemas** (`app/schemas/`): Pydantic validation schemas for request/response data
- **Core** (`app/core/`): Security (JWT, password hashing), configuration (env vars)
- **Database** (`app/db/`): SQLAlchemy engine, session management, Supabase SSL config

## Critical Data Flow

1. **Authentication**: User credentials → `auth.py` → password hashed with Argon2 → JWT token created → stored in HTTP-only cookie
2. **Expense Operations**: Request with cookie token → `get_current_user()` extracts username from JWT → query UserDB to get user ID → filter ExpenseDB by owner_id
3. **Session Management**: Every endpoint receives `db: Session = Depends(get_db)` from FastAPI dependency injection

## Key Patterns & Conventions

### Token & Session Management
- Tokens stored in **HTTP-only cookies** (not headers), set in login response
- `get_current_user(request: Request)` extracts token from request cookies, decodes JWT
- Always look up user by username after token validation to get user ID for isolation
- All expense queries filtered by `owner_id` to enforce data isolation

### Database & ORM
- Tables use `__tablename__` (users, expenses) with snake_case, not camelCase
- Timestamps use `Column(DateTime, default=datetime.utcnow)` (UTC times)
- Foreign keys: `owner_id = Column(Integer, ForeignKey("users.id"))`
- Queries always call `.first()` or `.all()` to execute; use `.filter()` with multiple conditions via comma separation
- Pattern: `db.query(Model).filter(Condition1, Condition2).first()`

### Schema Validation
- Request schemas (`CreateExpense`, `UpdateExpense`) use optional fields for updates with `Optional[type] = None`
- Response schemas inherit `from_attributes = True` in Config for SQLAlchemy model conversion
- Use `Field(..., gt=0)` for positive amounts, `Field(..., min_length=1)` for required strings

### Routing
- Routers use `prefix="/api"` and `tags=["endpoint_category"]` for documentation grouping
- Include routers in `main.py` with `app.include_router()`
- Dependencies always pass: `Depends(get_db)`, `Depends(get_current_user)`

## Environment & Configuration

- **Config source**: `app/core/config.py` loads from `.env` via `python-dotenv`
- **Required vars**: `SECRET_KEY` (JWT signing), `DATABASE_URL` (PostgreSQL/Supabase connection string)
- **Supabase-specific**: Database uses `sslmode="require"`, socket IPv4 patching, connection pooling (pool_size=5)
- Raises `ValueError` on missing critical environment variables at import time

## Developer Workflows

### Running Locally
```bash
pip install -r requirements.txt
python run.py  # Runs uvicorn on default host/port
```

### Database Initialization
- `init_db.py` creates tables; also runs on app startup via `Base.metadata.create_all(bind=engine)` in `startup_event`
- SQLAlchemy models define schema; no separate migrations (for simple deploys)

### Testing Endpoints
- OpenAPI docs at `/docs` (Swagger UI) auto-generated from type hints and schemas
- JWT cookie set in login; subsequent requests auto-use cookie (browser/API client aware)

## Common Modifications

**Adding a new endpoint:**
1. Create schema in `app/schemas/` with Pydantic models
2. Add DB model in `app/models/` if new table
3. Define route in `app/routes/` with `@router.post|get|put|delete()` and `Depends()` injection
4. Use `Depends(get_current_user)` to require auth; `Depends(get_db)` for DB access
5. Include router in `main.py`

**Password hashing & verification:**
- Use `get_password_hash(password: str)` and `verify_password(plain, hashed)` from `security.py`
- Never store plain passwords; only hashed_password in UserDB

**Cross-origin requests:**
- CORS enabled for all origins (`allow_origins=["*"]`) in `main.py`; adjust for production

## Dependencies

- **FastAPI** (0.104.1): Web framework, auto docs, dependency injection
- **SQLAlchemy** (2.0.23): ORM for database abstraction
- **python-jose**: JWT creation/validation
- **argon2-cffi**: Password hashing (industry standard)
- **pydantic** (2.5.0): Request/response validation
- **python-dotenv**: Environment variable loading
