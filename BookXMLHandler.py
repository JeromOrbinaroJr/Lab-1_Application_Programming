import xml.etree.ElementTree as ET
from typing import Optional
from Author import Author
from Book import Book

class BookXMLHandler:
    def __init__(self, filepath: str):
        self.filepath =filepath

    def create(self, book: Book):
        root = ET.Element("books")
        book_element = ET.SubElement(root, "book")
        ET.SubElement(book_element, "title").text = book.title
        ET.SubElement(book_element, "author").text = book.author.name if book.author else "Unknown"
        ET.SubElement(book_element, "price").text = str(book.price)
        ET.SubElement(book_element, "quantity").text = str(book.quantity)

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, title: str) -> Optional[Book]:
        tree = ET.parse(self.filepath)
        root = tree.getroot()

        for book_element in root.findall("book"):
            if book_element.find("title").text == title:
                author_name = book_element.find("author").text
                price = float(book_element.find("price").text)
                quantity = int(book_element.find("quantity").text)
                return Book(title, Author(author_name), price, quantity)

    def update(self, title: str, new_price: float, new_quantity: int):
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        for book_element in root.findall("book"):
            if book_element.find("title").text == title:
                book_element.find("price").text = str(new_price)
                book_element.find("quantity").text = str(new_quantity)
                tree.write(self.filepath)
                return True
        return False

    def delete(self, title: str):
        tree = ET.parse(self.filepath)
        root = tree.getroot()

        for book_element in root.findall("book"):
            if book_element.find("title").text == title:
                root.remove(book_element)
                tree.write(self.filepath)
                return True
        return False