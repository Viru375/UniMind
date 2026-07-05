from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt

router = APIRouter()

SECRET_KEY = "unimind_super_secret_key_for_hackathon"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=24)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup")
def signup(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"message": f"User {form_data.username} successfully registered for UniMind!"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}