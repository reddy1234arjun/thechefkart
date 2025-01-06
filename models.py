from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import BigInteger, Boolean, Column, Integer, String, Text, ForeignKey, JSON, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    mobilenumber = Column(BigInteger, nullable=False, unique=True)
    address = Column(Text, nullable=True)
    postcount = Column(Integer, default=0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)  
    title = Column(Text, nullable=False) 
    description = Column(Text, nullable=False) 
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  
    images = Column(JSON, nullable=True) 
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="posts")


class UserCreate(BaseModel):
    name: str
    mobilenumber: int
    address: str

class UserResponse(BaseModel):
    id: int
    name: str
    mobilenumber: int
    address: str
    postcount: int
   

class PostCreate(BaseModel):
    title: str
    description: str
    user_id: int
    images: Optional[List[str]] = None

class PostResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int
    images: Optional[List[str]] = None