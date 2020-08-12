import databases
import sqlalchemy
from fastapi import FastAPI
from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from fastapi_users.db import BaseUserDatabase
from fastapi_users.authentication import CookieAuthentication
from fastapi_users import FastAPIUsers
from fastapi_users.password import get_password_hash

from ..settings import Settings
settings=Settings()

SECRET = settings.SECRET_KEY

auth_backends = []

cookie_authentication = CookieAuthentication(secret=SECRET, lifetime_seconds=3600, cookie_secure=False)

auth_backends.append(cookie_authentication)

class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

database = databases.Database(DATABASE_URL)

Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

Base.metadata.create_all(engine)

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)

app = FastAPI()

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

get_active_user = fastapi_users.get_current_active_user
get_auth_router = fastapi_users.get_auth_router
get_password_hash = get_password_hash

async def user_create(UD):
    await fastapi_users.db.create(UD)
