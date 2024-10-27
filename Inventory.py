from typing import List
from Book import Book

class Inventory:
    def __init__(self):
        self.books: List[Book] = []

    def add_book(self, book: Book):
        self.books.append(book)

    def remove_book(self, title: str):
        self.books = [book for book in self.books if book.title != title]

    def find_book_by_title(self, title: str) -> Book:
        for book in self.books:
            if book.title == title:
                return book
        raise ValueError(f"Book titled '{title}' not found.")

    def list_books(self):
        return [str(book) for book in self.books]

    def check_stock(self, title: str) -> int:
        book = self.find_book_by_title(title)
        return book.quantity

    def update_stock(self, title: str, new_quantity: int):
        book = self.find_book_by_title(title)
        book.update_quantity(new_quantity)
