from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.users.interfaces.user_interfaces import UserCreate, UserRead, UserWithPassword


class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, id: UUID) -> UserRead:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserWithPassword:
        pass

    @abstractmethod
    def create_user(self, user_data: UserCreate) -> UserRead:
        pass
