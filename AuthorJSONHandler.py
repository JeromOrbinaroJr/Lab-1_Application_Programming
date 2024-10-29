import json
from typing import Optional
from Author import Author

class AuthorJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, author: Author):
        author_data = {
            "name": author.name,
            "birthdate": author.birthdate
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"authors": []}

        data["authors"].append(author_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, name: str) -> Optional[Author]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for author_data in data.get("authors", []):
                if author_data["name"] == name:
                    return Author(author_data["name"], author_data["birthdate"])
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update(self, name: str, new_birthdate: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for author_data in data.get("authors", []):
                if author_data["name"] == name:
                    author_data["birthdate"] = new_birthdate
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        return False

    def delete(self, name: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            data["authors"] = [author for author in data.get("authors", []) if author["name"] != name]
            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False