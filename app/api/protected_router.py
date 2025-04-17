from fastapi import APIRouter

from app.modules.books.book_routes import book_router


protected_router = APIRouter()

protected_router.include_router(book_router, prefix='/book')
