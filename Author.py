from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from Book import Book

class BookAlreadyAdded(Exception):
    pass

class Author:
    def __init__(self, name: str, birthdate: str):
        assert isinstance(name, str) and name, "Author name must be a non-empty string"
        assert isinstance(birthdate, str) and birthdate, "Birthdate must be a non-empty string"

        self.name = name
        self.birthdate = birthdate
        self.books: List["Book"] = []

    def add_book(self, book: "Book"):
        try:
            if book not in self.books:
                self.books.append(book)
                book.author = self
            else:
                raise BookAlreadyAdded(f"{book} already added to the author: {self.name}.")
        except BookAlreadyAdded as e:
            print(e)
            return False

    def __str__(self):
        book_titles = [book.title for book in self.books]
        return f"Author(name={self.name}, birthdate={self.birthdate}, books={book_titles})"
