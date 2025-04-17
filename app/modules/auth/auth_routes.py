from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.db.engine import get_session
from app.modules.auth.controllers.auth_controller import AuthController
from app.modules.auth.interfaces.token_interfaces import Token
from app.modules.users.interfaces.user_interfaces import UserCreate, UserRead


auth_router = APIRouter()

@auth_router.post('/signup', response_model=UserRead)
def signup(*,
           session: Session = Depends(get_session),
           user_data: UserCreate):
    new_user = AuthController(session).signup(user_data)
    return new_user


@auth_router.post('/login', response_model=Token)
def login(
    *,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    token = AuthController(session).login(form_data.username, form_data.password)
    return token
