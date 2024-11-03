import xml.etree.ElementTree as ET
from typing import Optional
from Author import Author

class AuthorExistsError(Exception):
    pass

class AuthorNotFoundError(Exception):
    pass

class AuthorXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, author: Author):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("authors")

        for author_element in root.findall("author"):
            if author_element.find("name").text == author.name:
                raise AuthorExistsError(f"Author '{author.name}' already exists.")

        author_element = ET.SubElement(root, "author")
        ET.SubElement(author_element, "name").text = author.name
        ET.SubElement(author_element, "birthdate").text = author.birthdate

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, name: str) -> Optional[Author]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for author_element in root.findall("author"):
                if author_element.find("name").text == name:
                    birthdate = author_element.find("birthdate").text
                    return Author(name, birthdate)
        except (FileNotFoundError, ET.ParseError):
            return None
        return None

    def update(self, name: str, new_birthdate: str) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for author_element in root.findall("author"):
                if author_element.find("name").text == name:
                    author_element.find("birthdate").text = new_birthdate
                    tree.write(self.filepath)
                    return True

            raise AuthorNotFoundError(f"Author '{name}' not found for update.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except AuthorNotFoundError as e:
            print(e)
            return False

    def delete(self, name: str) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for author_element in root.findall("author"):
                if author_element.find("name").text == name:
                    root.remove(author_element)
                    tree.write(self.filepath)
                    return True

            raise AuthorNotFoundError(f"Author '{name}' not found for deletion.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except AuthorNotFoundError as e:
            print(e)
            return False
