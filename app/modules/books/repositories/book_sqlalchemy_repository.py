from typing import List

from sqlmodel import select, Session

from app.modules.books.interfaces.book_errors import BookNotFound
from app.modules.books.interfaces.book_interfaces import BookCreate, BookRead, BookUpdate
from app.modules.books.interfaces.book_repository import BookRepository
from app.modules.books.models.book import Book


class BookSQLAlchemyRepository(BookRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_books_list(self, page: int, page_size: int) -> List[BookRead]:
        query = select(Book).offset((page-1)*page_size).limit(page_size)
        books = self._session.exec(query).all()
        return list(books)

    def get_book_by_id(self, id) -> BookRead | None:
        book = self._session.get(Book, id)
        if book is None:
            raise BookNotFound()
        return book

    def create_book(self, book_data: BookCreate) -> BookRead:
        book = Book(**book_data.model_dump())
        self._session.add(book)
        self._session.commit()
        self._session.refresh(book)
        return BookRead(**book.model_dump())

    def update_book(self, id: int, book_data: BookUpdate) -> BookRead:
        book = self._session.get(Book, id)
        if book is None:
            raise BookNotFound()
        for field, value in book_data.model_dump(exclude_none=True).items():
            setattr(book, field, value)
        self._session.add(book)
        self._session.commit()
        self._session.refresh(book)
        return BookRead(**book.model_dump())

    def delete_book(self, id: int) -> None:
        book = self._session.get(Book, id)
        if book is None:
            raise BookNotFound()
        self._session.delete(book)
        self._session.commit()
