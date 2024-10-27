from typing import List
from Book import Book

class Author:
    def __init__(self, name: str, birthdate: str):
        assert isinstance(name, str) and name, "Author name must be a non-empty string"
        assert isinstance(birthdate, str) and birthdate, "Birthdate must be a non-empty string"

        self.name = name
        self.birthdate = birthdate
        self.books: List[Book] = []

    def add_book(self, book: Book):
        try:
            if not isinstance(book, Book):
                raise TypeError("Expected an instance of Book.")

            if book in self.books:
                raise ValueError(f"The book '{book.title}' is already associated with {self.name}.")

            self.books.append(book)
            book.author = self

        except TypeError as te:
            print(f"TypeError: {te}")
        except ValueError as ve:
            print(f"ValueError: {ve}")

    def __str__(self):
        book_titles = [book.title for book in self.books]
        return f"Author(name={self.name}, birthdate={self.birthdate}, books={book_titles})"
