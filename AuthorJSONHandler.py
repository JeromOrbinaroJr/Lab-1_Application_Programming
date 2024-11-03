import json
from typing import Optional
from Author import Author

class AuthorExistsError(Exception):
    pass
class AuthorNotFoundError(Exception):
    pass

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

        for existing_author in data.get("authors", []):
            if existing_author["name"] == author.name:
                raise AuthorExistsError(f"Author '{author.name}' already exists.")

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
            raise AuthorNotFoundError(f"Author '{name}' not found for update.")
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except AuthorNotFoundError as e:
            print(e)
            return False

    def delete(self, name: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("authors", []))
            data["authors"] = [author for author in data.get("authors", []) if author["name"] != name]

            if len(data["authors"]) == original_length:
                raise AuthorNotFoundError(f"Author '{name}' not found for deletion.")

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except AuthorNotFoundError as e:
            print(e)
            return False
