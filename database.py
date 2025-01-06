from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DATABASE_URL

# Validate database URLs
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set.")

# Create engine and session maker for DATABASE_URL
engine = create_engine(
    DATABASE_URL,
    pool_size=30,        # Maintain 20 connections in the pool
    max_overflow=10,      # No additional connections beyond pool_size
    pool_timeout=30,     # Timeout for obtaining a connection from the pool (seconds)
    pool_recycle=3600    # Time after which connections are recycled (seconds)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Initialize tables for DATABASE_URL
def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

init_db()
