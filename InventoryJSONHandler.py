import json
from typing import Optional
from Inventory import Inventory
from Book import Book


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

        data["books"].append(book_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

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
            inventory = self.read()
            for idx, inv_book in enumerate(inventory.books):
                if inv_book.title == book.title:
                    inventory.books[idx] = book
                    break
            self.write_inventory(inventory)
        except Exception as e:
            print(f"Error updating JSON: {e}")

    def delete(self, title: str):
        try:
            inventory = self.read()
            inventory.remove_book(title)
            self.write_inventory(inventory)
        except Exception as e:
            print(f"Error deleting JSON: {e}")

    def write_inventory(self, inventory: Inventory):
        data = {"books": []}
        for book in inventory.books:
            book_data = {
                "title": book.title,
                "author": book.author,
                "price": book.price,
                "quantity": book.quantity
            }
            data["books"].append(book_data)

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)
