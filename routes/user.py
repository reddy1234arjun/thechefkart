import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from database import get_db
from models import User, UserCreate, UserResponse

router = APIRouter(tags=["User"])

@router.post("/create-users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        if not user.name.isalpha():
            raise HTTPException(status_code=400, detail="Name must contain only alphabetic characters.")
        
        # Mobile number validation
        mobilenumber = str(user.mobilenumber)  # Convert to string for validation
        if not (mobilenumber.startswith(('6', '7', '8', '9'))):
            raise HTTPException(status_code=400, detail="Mobile number must start with 6, 7, 8, or 9.")
        
        # Check for sequential numbers in mobile number
        if re.search(r'123456|234567|345678|456789|567890|678901|789012|890123|901234', mobilenumber):
            raise HTTPException(status_code=400, detail="Mobile number cannot be a sequence of numbers.")
        
        # Check if the mobile number already exists
        existing_user = db.query(User).filter(User.mobilenumber == user.mobilenumber).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Mobile number already registered.")
        
        new_user = User(
            name=user.name,
            mobilenumber=user.mobilenumber,
            address=user.address,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/get-user/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/get-all-users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")