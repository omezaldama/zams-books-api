from uuid import UUID

from sqlmodel import select, Session
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.modules.users.interfaces.user_errors import UserNotFound, UserWithEmailAlreadyExists
from app.modules.users.interfaces.user_interfaces import UserCreate, UserRead, UserWithPassword
from app.modules.users.interfaces.user_repository import UserRepository
from app.modules.users.models.user import User


class UserSQLAlchemyRepository(UserRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_user_by_id(self, id: UUID):
        user = self._session.get(User, id)
        if user is None:
            raise UserNotFound()
        return user

    def get_user_by_email(self, email: str) -> UserWithPassword:
        query = select(User).where(User.email == email)
        try:
            user = self._session.exec(query).one()
            return user
        except NoResultFound:
            raise UserNotFound()

    def create_user(self, user_data: UserCreate) -> UserRead:
        try:
            user = User(**user_data.model_dump())
            self._session.add(user)
            self._session.commit()
            self._session.refresh(user)
            return UserRead(**user.model_dump())
        except IntegrityError:
            raise UserWithEmailAlreadyExists()
