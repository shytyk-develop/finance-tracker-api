from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
import socket

from app.core.config import SQLALCHEMY_DATABASE_URL

# Force IPv4 for Vercel compatibility
def patched_getaddrinfo(host, port, *args, **kwargs):
    return socket.getaddrinfo(host, port, socket.AF_INET, *args[1:], **kwargs)

socket.getaddrinfo = patched_getaddrinfo

# Supabase-specific connection configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10,
    },
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=0,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
