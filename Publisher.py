from typing import List
from Book import Book

class Publisher:
    def __init__(self, name: str):
        self.name = name
        self.books_published: List[Book] = []

    def publish_book(self, book: Book):
        if book not in self.books_published:
            self.books_published.append(book)
        else:
            print(f"The book '{book.title}' is already published by {self.name}")

    def get_published_books(self) -> List[str]:
        return [book.title for book in self.books_published]

    def __str__(self):
        book_titles = [book.title for book in self.books_published]
        return f"Publisher(name={self.name}, books_published={book_titles})"
