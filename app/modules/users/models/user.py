import uuid

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(nullable=False, index=True, unique=True)
    password: str = Field(nullable=False)
