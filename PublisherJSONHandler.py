import json
from typing import Optional
from Publisher import Publisher
from Book import Book

class PublisherExistsError(Exception):
    pass

class PublisherNotFoundError(Exception):
    pass

class PublisherJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, publisher: Publisher):
        publisher_data = {
            "name": publisher.name,
            "books_published": [
                {"title": book.title, "author": book.author, "price": book.price, "quantity": book.quantity}
                for book in publisher.books_published
            ]
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"publishers": []}

        for existing_publisher in data.get("publishers", []):
            if existing_publisher["name"] == publisher.name:
                raise PublisherExistsError(f"Publisher '{publisher.name}' already exists.")

        data["publishers"].append(publisher_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, name: str) -> Optional[Publisher]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for publisher_data in data.get("publishers", []):
                if publisher_data["name"] == name:
                    publisher = Publisher(publisher_data["name"])
                    for book_data in publisher_data["books_published"]:
                        book = Book(book_data["title"], book_data["author"], book_data["price"], book_data["quantity"])
                        publisher.publish_book(book)
                    return publisher
            raise PublisherNotFoundError(f"Publisher '{name}' not found.")
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update(self, publisher: Publisher) -> bool:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for idx, publisher_data in enumerate(data["publishers"]):
                if publisher_data["name"] == publisher.name:
                    data["publishers"][idx] = {
                        "name": publisher.name,
                        "books_published": [
                            {"title": book.title, "author": book.author, "price": book.price, "quantity": book.quantity}
                            for book in publisher.books_published
                        ]
                    }
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
            raise PublisherNotFoundError(f"Publisher '{publisher.name}' not found for update.")
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except PublisherNotFoundError as e:
            print(e)
            return False

    def delete(self, name: str) -> bool:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("publishers", []))
            data["publishers"] = [pub for pub in data.get("publishers", []) if pub["name"] != name]

            if len(data["publishers"]) == original_length:
                raise PublisherNotFoundError(f"Publisher '{name}' not found for deletion.")

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except PublisherNotFoundError as e:
            print(e)
            return False
