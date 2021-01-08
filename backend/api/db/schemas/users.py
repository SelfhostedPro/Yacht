from pydantic import BaseModel
from uuid import UUID
from typing import Union


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: Union[int, str, UUID]
    is_active: bool

    class Config:
        orm_mode = True
