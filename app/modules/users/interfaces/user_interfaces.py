from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserRead(UserBase):
    id: UUID


class UserWithPassword(UserRead):
    password: str


class UserCreate(UserBase):
    password: str
