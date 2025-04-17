from datetime import date
from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    published_date: Optional[date] = None
    summary: Optional[str] = None
    genre: str


class BookRead(BookBase):
    id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[date] = None
    summary: Optional[str] = None
    genre: Optional[str] = None
