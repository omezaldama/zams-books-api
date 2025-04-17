from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.engine import get_session
from app.modules.books.controllers.books_controller import BooksController
from app.modules.books.interfaces.book_interfaces import BookCreate, BookRead, BookUpdate


book_router = APIRouter()

@book_router.get('/', response_model=List[BookRead])
def get_books_list(*,
                   session: Session = Depends(get_session),
                   page: int = 1,
                   page_size: int = 10):
    books = BooksController(session).get_books_list(page, page_size)
    return books


@book_router.get('/{id}', response_model=BookRead)
def get_book_by_id(*,
                   session: Session = Depends(get_session),
                   id: int):
    book = BooksController(session).get_book_by_id(id)
    return book


@book_router.post('/', response_model=BookRead)
def create_book(*,
                session: Session = Depends(get_session),
                book_data: BookCreate):
    book = BooksController(session).create_book(book_data)
    return book


@book_router.patch('/{id}', response_model=BookRead)
def update_book(*,
                session: Session = Depends(get_session),
                id: int,
                book_data: BookUpdate):
    book = BooksController(session).update_book(id, book_data)
    return book


@book_router.delete('/{id}')
def delete_book(*,
                session: Session = Depends(get_session),
                id: int):
    BooksController(session).delete_book(id)
