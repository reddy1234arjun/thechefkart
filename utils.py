
from passlib.hash import bcrypt
from dotenv import load_dotenv

from database import SessionLocal

# Load environment variables from .env file
load_dotenv("credentials.env")

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

