import xml.etree.ElementTree as ET
from typing import Optional
from Author import Author

class AuthorXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, author: Author):
        root = ET.Element("authors")
        author_element = ET.SubElement(root, "author")
        ET.SubElement(author_element, "name").text = author.name
        ET.SubElement(author_element, "birthdate").text = author.birthdate

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, name: str) -> Optional[Author]:
        tree = ET.parse(self.filepath)
        root = tree.getroot()

        for author_element in root.findall("author"):
            if author_element.find("name").text == name:
                birthdate = author_element.find("birthdate").text
                return Author(name, birthdate)
        return None

    def update(self, name: str, new_birthdate: str):
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        for author_element in root.findall("author"):
            if author_element.find("name").text == name:
                author_element.find("birthdate").text = new_birthdate
                tree.write(self.filepath)
                return True
        return False

    def delete(self, name: str):
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        for author_element in root.findall("author"):
            if author_element.find("name").text == name:
                root.remove(author_element)
                tree.write(self.filepath)
                return True
        return False
