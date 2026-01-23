from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import API_TITLE, API_DESCRIPTION, API_VERSION
from app.db.database import Base, engine
from app.routes import auth, expenses

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(expenses.router)


@app.get("/")
def root():
    return {"message": "Welcome to Expense Tracker API"}


@app.on_event("startup")
def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Database initialization warning: {e}")
        pass
