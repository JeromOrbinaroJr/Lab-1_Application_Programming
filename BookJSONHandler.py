import json
from typing import Optional

from Author import Author
from Book import Book

class BookJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, book: Book):
        book_data = {
            "title": book.title,
            "author": book.author.name if book.author else "Unknown",
            "price": book.price,
            "quantity": book.quantity
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"books": []}

        data["books"].append(book_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, title: str) -> Optional[Book]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for book_data in data.get("books", []):
                if book_data["title"] == title:
                    author_name = book_data["author"]
                    price = book_data["price"]
                    quantity = book_data["quantity"]
                    return Book(title, Author(author_name), price, quantity)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update(self, title: str, new_price: float, new_quantity: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for book_data in data.get("books", []):
                if book_data["title"] == title:
                    book_data["price"] = new_price
                    book_data["quantity"] = new_quantity
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        return False

    def delete(self, title: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            data["books"] = [book for book in data.get("books", []) if book["title"] != title]
            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False