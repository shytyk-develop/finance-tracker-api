import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import API_TITLE, API_DESCRIPTION, API_VERSION
from app.db.database import Base, engine
from app.routes import auth, expenses
from app.core.limiter import limiter 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://income-tracker-frontend-five.vercel.app",   
        "http://localhost:3000",                            
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error occurred: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )

app.include_router(auth.router)
app.include_router(expenses.router)

@app.get("/")
@limiter.limit("10/minute")
def root(request: Request):
    return {"message": "Welcome to Expense Tracker API"}

@app.on_event("startup")
def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.") 
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")