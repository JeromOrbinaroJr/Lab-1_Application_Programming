import xml.etree.ElementTree as ET
from typing import Optional
from Inventory import Inventory
from Book import Book

class InventoryXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, book: Book):
        try:
            root = ET.Element("inventory")
            book_element = ET.SubElement(root, "book")
            ET.SubElement(book_element, "title").text = book.title
            ET.SubElement(book_element, "author").text = book.author
            ET.SubElement(book_element, "price").text = str(book.price)
            ET.SubElement(book_element, "quantity").text = str(book.quantity)

            tree = ET.ElementTree(root)
            tree.write(self.filepath)
        except Exception as e:
            print(f"Error creating XML: {e}")

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
        except Exception as e:
            print(f"Error reading XML: {e}")
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
            print(f"Error updating XML: {e}")

    def delete(self, title: str):
        try:
            inventory = self.read()
            inventory.remove_book(title)
            self.write_inventory(inventory)
        except Exception as e:
            print(f"Error deleting XML: {e}")

    def write_inventory(self, inventory: Inventory):
        root = ET.Element("inventory")
        for book in inventory.books:
            book_element = ET.SubElement(root, "book")
            ET.SubElement(book_element, "title").text = book.title
            ET.SubElement(book_element, "author").text = book.author
            ET.SubElement(book_element, "price").text = str(book.price)
            ET.SubElement(book_element, "quantity").text = str(book.quantity)

        tree = ET.ElementTree(root)
        tree.write(self.filepath)
