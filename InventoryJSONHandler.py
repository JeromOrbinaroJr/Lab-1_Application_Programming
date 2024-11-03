import json
from typing import Optional
from Inventory import Inventory
from Book import Book

class BookExistsError(Exception):
    pass

class BookNotFoundError(Exception):
    pass

class InventoryJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, book: Book):
        book_data = {
            "title": book.title,
            "author": book.author,
            "price": book.price,
            "quantity": book.quantity
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"books": []}

        if any(b["title"] == book.title for b in data["books"]):
            raise BookExistsError(f"Book '{book.title}' already exists.")

        data["books"].append(book_data)
        self.write_inventory(data)

    def read(self) -> Inventory:
        inventory = Inventory()
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for book_data in data.get("books", []):
                book = Book(book_data["title"], book_data["author"], book_data["price"], book_data["quantity"])
                inventory.add_book(book)
            return inventory
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error reading JSON: file not found or invalid format.")
            return inventory

    def update(self, book: Book):
        try:
            data = self.read().books
            for b in data:
                if b.title == book.title:
                    b.author = book.author
                    b.price = book.price
                    b.quantity = book.quantity
                    self.write_inventory(data)
                    return
            raise BookNotFoundError(f"Book '{book.title}' not found for update.")
        except Exception as e:
            print(f"Error updating JSON: {e}")

    def delete(self, title: str):
        try:
            data = self.read().books
            if not any(b.title == title for b in data):
                raise BookNotFoundError(f"Book '{title}' not found for deletion.")
            data = [b for b in data if b.title != title]
            self.write_inventory(data)
        except Exception as e:
            print(f"Error deleting JSON: {e}")

    def write_inventory(self, data):
        with open(self.filepath, "w") as file:
            json.dump({"books": data}, file, indent=4)
