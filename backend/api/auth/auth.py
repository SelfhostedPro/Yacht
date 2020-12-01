from typing import Tuple

from ..settings import Settings

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from passlib import pwd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

settings = Settings()


def verify_and_update_password(
    plain_password: str, hashed_password: str
) -> Tuple[bool, str]:
    return pwd_context.verify_and_update(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_password() -> str:
    return pwd.genword()

def auth_check(Authorize):
    if settings.DISABLE_AUTH == "True":
        return
    else:
        return Authorize.jwt_required()