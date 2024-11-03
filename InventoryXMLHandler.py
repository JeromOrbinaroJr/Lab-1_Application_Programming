import xml.etree.ElementTree as ET
from typing import Optional
from Inventory import Inventory
from Book import Book

class BookExistsError(Exception):
    pass

class BookNotFoundError(Exception):
    pass

class InventoryXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, book: Book):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("inventory")

        if any(b.find("title").text == book.title for b in root.findall("book")):
            raise BookExistsError(f"Book '{book.title}' already exists.")

        book_element = ET.SubElement(root, "book")
        ET.SubElement(book_element, "title").text = book.title
        ET.SubElement(book_element, "author").text = book.author
        ET.SubElement(book_element, "price").text = str(book.price)
        ET.SubElement(book_element, "quantity").text = str(book.quantity)

        self.write_inventory(root)

    def read(self) -> Inventory:
        inventory = Inventory()
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for book_element in root.findall("book"):
                title = book_element.find("title").text
                author = book_element.find("author").text
                price = float(book_element.find("price").text)
                quantity = int(book_element.find("quantity").text)
                book = Book(title, author, price, quantity)
                inventory.add_book(book)
            return inventory
        except (FileNotFoundError, ET.ParseError):
            print("Error reading XML: file not found or invalid format.")
            return inventory

    def update(self, book: Book):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for book_element in root.findall("book"):
                if book_element.find("title").text == book.title:
                    book_element.find("author").text = book.author
                    book_element.find("price").text = str(book.price)
                    book_element.find("quantity").text = str(book.quantity)
                    self.write_inventory(root)
                    return
            raise BookNotFoundError(f"Book '{book.title}' not found for update.")
        except (FileNotFoundError, ET.ParseError) as e:
            print(f"Error updating XML: {e}")

    def delete(self, title: str):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            found = False
            for book_element in root.findall("book"):
                if book_element.find("title").text == title:
                    root.remove(book_element)
                    found = True
                    break
            if not found:
                raise BookNotFoundError(f"Book '{title}' not found for deletion.")
            self.write_inventory(root)
        except (FileNotFoundError, ET.ParseError) as e:
            print(f"Error deleting XML: {e}")

    def write_inventory(self, root):
        tree = ET.ElementTree(root)
        tree.write(self.filepath)
