from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    _hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return(db_user)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)