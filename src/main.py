from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.responses import RedirectResponse  # Import RedirectResponse
from typing import Union
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware

# Define SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = 'register'
    name = Column(String,primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

class Users(Base):
    __tablename__ = 'login'
    email = Column(String, primary_key=True)
    password = Column(String)

# Create the database connection
DB_URL = 'postgresql://postgres:01477@localhost/master'
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Routes
@app.post('/register/')
def register_user(data: RegisterRequest):
    db = SessionLocal()
    user = User(name=data.name, email=data.email, password=data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"message": "Successfully registered"}

@app.post('/login/')
def login_user(data: LoginRequest, response: Response):
    db = SessionLocal()
    user = db.query(User).filter(User.email == data.email).first()
    db.close()
    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Redirect to next page if login is successful
    response = RedirectResponse(url='/next-page', status_code=303)
    return {"message":"Logged In"}
