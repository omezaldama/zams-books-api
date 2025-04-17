from datetime import datetime, timedelta, timezone
import os

from fastapi import HTTPException, status
from jose import jwt
from sqlmodel import Session

from app.modules.auth.interfaces.token_interfaces import Token
from app.modules.auth.middleware.jwt_middleware import ALGORITHM
from app.modules.auth.utils.password_utils import hash_password, verify_password
from app.modules.users.interfaces.user_errors import UserNotFound, UserWithEmailAlreadyExists
from app.modules.users.interfaces.user_interfaces import UserCreate, UserRead
from app.modules.users.repositories.user_sqlalchemy_repository import UserSQLAlchemyRepository


class AuthController:
    def __init__(self, session: Session):
        self._session = session

    def signup(self, user_data: UserCreate) -> UserRead:
        try:
            user_data.password = hash_password(user_data.password)
            new_user = UserSQLAlchemyRepository(self._session).create_user(user_data)
            return new_user
        except UserWithEmailAlreadyExists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='A user with that email already exists')

    def login(self, email: str, password: str) -> Token:
        try:
            user = UserSQLAlchemyRepository(self._session).get_user_by_email(email)
        except UserNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User does not exist')

        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Incorrect credentials')

        token = self._create_access_token({ 'uuid': str(user.id) })
        return Token(access_token=token, token_type='bearer')

    def _create_access_token(self, data: dict) -> str:
        token_expiration = int(os.getenv('TOKEN_EXPIRATION'))
        expires_delta = timedelta(minutes=token_expiration)
        expire = datetime.now(timezone.utc) + expires_delta

        to_encode = data.copy()
        to_encode.update({"exp": expire})

        secret_key = os.getenv('AUTH_SECRET_KEY')
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
        return encoded_jwt
