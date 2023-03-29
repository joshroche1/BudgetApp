from fastapi import Depends, APIRouter

from sqlalchemy.orm import Session

from .database import SessionLocal
from .auth import get_current_user, get_users, get_user_by_username


router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@router.get("/users/", tags=["users"])
async def get_users():
  users = get_users()
  return users

@router.get("/users/me", tags=["users"])
async def get_me():
  user = get_current_user()
  return user

@router.get("/users/{username}", tags=["users"])
async def get_user(username: str, db: Session = Depends(get_db)):
  user = get_user_by_username(db, username)
  return user
