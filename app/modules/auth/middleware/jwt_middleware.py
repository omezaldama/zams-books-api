import os
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session

from app.db.engine import get_session
from app.modules.users.interfaces.user_errors import UserNotFound
from app.modules.users.repositories.user_sqlalchemy_repository import UserSQLAlchemyRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
ALGORITHM = 'HS256'


def validate_token(token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, os.getenv('AUTH_SECRET_KEY'), algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid token')

    uuid: UUID = UUID(payload.get('uuid'))
    if uuid is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid token content')

    try:
        UserSQLAlchemyRepository(session).get_user_by_id(uuid)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid user')
