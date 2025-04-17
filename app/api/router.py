from fastapi import APIRouter, Depends

from app.api.protected_router import protected_router
from app.modules.auth.auth_routes import auth_router
from app.modules.auth.middleware.jwt_middleware import validate_token


main_router = APIRouter()

main_router.include_router(auth_router, prefix='/auth')
main_router.include_router(protected_router, prefix='/app', dependencies=[Depends(validate_token)])
