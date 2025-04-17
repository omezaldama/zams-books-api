from typing import List

from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.books.interfaces.book_errors import BookNotFound
from app.modules.books.interfaces.book_interfaces import BookCreate, BookRead, BookUpdate
from app.modules.books.repositories.book_sqlalchemy_repository import BookSQLAlchemyRepository


class BooksController:
    def __init__(self, session: Session):
        self._session = session

    def get_books_list(self, page: int, page_size: int) -> List[BookRead]:
        return BookSQLAlchemyRepository(self._session).get_books_list(page, page_size)

    def get_book_by_id(self, id: int) -> BookRead:
        try:
            book = BookSQLAlchemyRepository(self._session).get_book_by_id(id)
            return book
        except BookNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book not found')

    def create_book(self, book_data: BookCreate) -> BookRead:
        book = BookSQLAlchemyRepository(self._session).create_book(book_data)
        return book

    def update_book(self, id: int, book_data: BookUpdate) -> BookRead:
        try:
            book = BookSQLAlchemyRepository(self._session).update_book(id, book_data)
            return book
        except BookNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Book not found')

    def delete_book(self, id: int) -> None:
        try:
            BookSQLAlchemyRepository(self._session).delete_book(id)
        except BookNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Book not found')
