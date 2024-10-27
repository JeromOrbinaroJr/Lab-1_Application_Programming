from typing import List, Optional
from Book import Book

class Inventory:
    def __init__(self):
        self.books: List[Book] = []

    def add_book(self, book: Book):
        try:
            if not isinstance(book, Book):
                raise TypeError("Expected an instance of Book.")
            self.books.append(book)
        except TypeError as e:
            print(f"Error adding book: {e}")

    def remove_book(self, title: str):
        try:
            if not any(book.title == title for book in self.books):
                raise ValueError(f"Book titled '{title}' not found in inventory.")
            self.books = [book for book in self.books if book.title != title]
        except ValueError as e:
            print(e)

    def find_book_by_title(self, title: str) -> Optional[Book]:
        try:
            for book in self.books:
                if book.title == title:
                    return book
            raise ValueError(f"Book titled '{title}' not found.")
        except ValueError as e:
            print(e)
            return None

    def list_books(self):
        return [str(book) for book in self.books]

    def check_stock(self, title: str) -> int:
        try:
            book = self.find_book_by_title(title)
            if book:
                return book.quantity
            else:
                raise ValueError(f"Cannot check stock. Book titled '{title}' not found.")
        except ValueError as e:
            print(e)
            return 0

    def update_stock(self, title: str, new_quantity: int):
        try:
            if new_quantity < 0:
                raise ValueError("New quantity must be non-negative.")
            book = self.find_book_by_title(title)
            if book:
                book.update_quantity(new_quantity)
            else:
                raise ValueError(f"Cannot update stock. Book titled '{title}' not found.")
        except ValueError as e:
            print(e)
