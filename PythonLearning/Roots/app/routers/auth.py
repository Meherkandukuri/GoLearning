from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import jwt
import hashlib
from ..db import get_db
from ..config import settings

router = APIRouter()
security = HTTPBearer()

# Simple in-memory user storage (in production, use a proper database)
ADMIN_USERS = {
    "admin": {
        "username": "admin",
        "email": "admin@roots.com",
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin"
    }
}

# JWT Secret (in production, use a proper secret key)
JWT_SECRET = "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "valid": True}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/login")
async def login(credentials: dict):
    username = credentials.get("username")
    password = credentials.get("password")
    
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required"
        )
    
    # Check if user exists
    if username not in ADMIN_USERS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    user = ADMIN_USERS[username]
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if user["password_hash"] != password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@router.get("/verify")
async def verify_token_endpoint(token_data: dict = Depends(verify_token)):
    username = token_data["username"]
    user = ADMIN_USERS.get(username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return {
        "valid": True,
        "user": {
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@router.post("/logout")
async def logout():
    # In a stateless JWT system, logout is handled client-side
    # You could implement a token blacklist here if needed
    return {"message": "Successfully logged out"}
