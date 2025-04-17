from abc import ABC, abstractmethod
from typing import List

from app.modules.books.interfaces.book_interfaces import (
    BookCreate, BookRead, BookUpdate
)


class BookRepository(ABC):
    @abstractmethod
    def get_books_list(self, page: int, page_size: int) -> List[BookRead]:
        pass

    @abstractmethod
    def get_book_by_id(self, id: int) -> BookRead:
        pass

    @abstractmethod
    def create_book(self, book_data: BookCreate) -> BookRead:
        pass

    @abstractmethod
    def update_book(self, book_data: BookUpdate) -> BookRead:
        pass

    @abstractmethod
    def delete_book(self, id: int) -> None:
        pass
