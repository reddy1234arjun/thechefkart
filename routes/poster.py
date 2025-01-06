import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from database import get_db
from models import Post, PostCreate, PostResponse, User


router = APIRouter(tags=["post"])


@router.post("/create-posts/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        # Check if the user exists
        user = db.query(User).filter(User.id == post.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        if not re.match(r'^[a-zA-Z0-9\s]*$', post.title):
            raise HTTPException(status_code=400, detail="Title must only contain letters, numbers, and spaces.")
        
        # Validate that the description contains only letters and numbers
        if not re.match(r'^[a-zA-Z0-9\s]*$', post.description):
            raise HTTPException(status_code=400, detail="Description must only contain letters, numbers, and spaces.")
        new_post = Post(
            title=post.title,
            description=post.description,
            user_id=post.user_id,
            images=post.images,
        )
        db.add(new_post)
        user.postcount += 1
        db.commit()
        db.refresh(new_post)
        return new_post
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/get-posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found.")
        return post
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/get-all-posts/", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    try:
        posts = db.query(Post).all()
        return posts
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")