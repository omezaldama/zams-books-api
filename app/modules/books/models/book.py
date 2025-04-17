from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = 'books'

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    author: str = Field(nullable=False)
    published_date: Optional[date] = Field(nullable=True)
    summary: Optional[str] = Field(nullable=True)
    genre: str = Field(nullable=False)
