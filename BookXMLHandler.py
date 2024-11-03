import xml.etree.ElementTree as ET
from typing import Optional
from Author import Author
from Book import Book

class BookExistsError(Exception):
    pass

class BookNotFoundError(Exception):
    pass

class BookXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, book: Book):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("books")

        for book_element in root.findall("book"):
            if book_element.find("title").text == book.title:
                raise BookExistsError(f"Book '{book.title}' already exists.")

        book_element = ET.SubElement(root, "book")
        ET.SubElement(book_element, "title").text = book.title
        ET.SubElement(book_element, "author").text = book.author.name if book.author else "Unknown"
        ET.SubElement(book_element, "price").text = str(book.price)
        ET.SubElement(book_element, "quantity").text = str(book.quantity)

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, title: str) -> Optional[Book]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for book_element in root.findall("book"):
                if book_element.find("title").text == title:
                    author_name = book_element.find("author").text
                    price = float(book_element.find("price").text)
                    quantity = int(book_element.find("quantity").text)
                    return Book(title, Author(author_name), price, quantity)
        except (FileNotFoundError, ET.ParseError):
            return None
        return None

    def update(self, title: str, new_price: float, new_quantity: int) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for book_element in root.findall("book"):
                if book_element.find("title").text == title:
                    book_element.find("price").text = str(new_price)
                    book_element.find("quantity").text = str(new_quantity)
                    tree.write(self.filepath)
                    return True
            raise BookNotFoundError(f"Book '{title}' not found for update.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except BookNotFoundError as e:
            print(e)
            return False

    def delete(self, title: str) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for book_element in root.findall("book"):
                if book_element.find("title").text == title:
                    root.remove(book_element)
                    tree.write(self.filepath)
                    return True
            raise BookNotFoundError(f"Book '{title}' not found for deletion.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except BookNotFoundError as e:
            print(e)
            return False
