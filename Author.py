from typing import List
from Book import Book

class Author:
    def __init__(self, name: str, birthdate: str):
        self.name = name
        self.birthdate = birthdate
        self.books: List[Book] = []

    def add_book(self, book: Book):
        if book not in self.books:
            self.books.append(book)
            book.author = self
        else:
            print(f"The book '{book.title}' already belongs to {self.name}")

    def __str__(self):
        book_titles = [book.title for book in self.books]
        return f"Author(name={self.name}, birthdate={self.birthdate}, books={book_titles})"
