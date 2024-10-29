import json
from Publisher import Publisher
from Book import Book

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

        data["publishers"].append(publisher_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, name: str) -> Publisher:
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
            print(f"Publisher '{name}' not found.")
            return None
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error reading JSON: file not found or invalid format.")
            return None

    def update(self, publisher: Publisher):
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
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error updating JSON: file not found or invalid format.")
            return False
        return False

    def delete(self, name: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            data["publishers"] = [pub for pub in data.get("publishers", []) if pub["name"] != name]
            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error deleting JSON: file not found or invalid format.")
            return False
