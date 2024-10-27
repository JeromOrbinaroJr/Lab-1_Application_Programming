from typing import List
from Book import Book

class Publisher:
    def __init__(self, name: str):
        assert isinstance(name, str) and name, "Publisher name must be a non-empty string."
        self.name = name
        self.books_published: List[Book] = []

    def publish_book(self, book: Book):
        try:
            assert isinstance(book, Book), "The book must be an instance of the Book class."
            if book not in self.books_published:
                self.books_published.append(book)
            else:
                print(f"The book '{book.title}' is already published by {self.name}")
        except AssertionError as e:
            print(f"Error in publish_book: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_published_books(self) -> List[str]:
        try:
            book_titles = [book.title for book in self.books_published]
            return book_titles
        except Exception as e:
            print(f"An error occurred while retrieving published books: {e}")
            return []

    def __str__(self):
        book_titles = [book.title for book in self.books_published]
        return f"Publisher(name={self.name}, books_published={book_titles})"