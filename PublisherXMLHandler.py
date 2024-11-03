import xml.etree.ElementTree as ET
from typing import Optional
from Publisher import Publisher
from Book import Book

class PublisherExistsError(Exception):
    pass

class PublisherNotFoundError(Exception):
    pass

class PublisherXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, publisher: Publisher):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("publishers")

        for publisher_element in root.findall("publisher"):
            if publisher_element.find("name").text == publisher.name:
                raise PublisherExistsError(f"Publisher '{publisher.name}' already exists.")

        publisher_element = ET.SubElement(root, "publisher")
        ET.SubElement(publisher_element, "name").text = publisher.name

        books_element = ET.SubElement(publisher_element, "books_published")
        for book in publisher.books_published:
            book_element = ET.SubElement(books_element, "book")
            ET.SubElement(book_element, "title").text = book.title
            ET.SubElement(book_element, "author").text = book.author
            ET.SubElement(book_element, "price").text = str(book.price)
            ET.SubElement(book_element, "quantity").text = str(book.quantity)

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, name: str) -> Optional[Publisher]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for publisher_element in root.findall("publisher"):
                if publisher_element.find("name").text == name:
                    publisher = Publisher(name)
                    books_element = publisher_element.find("books_published")
                    for book_element in books_element.findall("book"):
                        title = book_element.find("title").text
                        author = book_element.find("author").text
                        price = float(book_element.find("price").text)
                        quantity = int(book_element.find("quantity").text)
                        book = Book(title, author, price, quantity)
                        publisher.publish_book(book)
                    return publisher
            raise PublisherNotFoundError(f"Publisher '{name}' not found.")
        except (FileNotFoundError, ET.ParseError):
            return None
        except PublisherNotFoundError as e:
            print(e)
            return None

    def update(self, publisher: Publisher) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for publisher_element in root.findall("publisher"):
                if publisher_element.find("name").text == publisher.name:
                    publisher_element.find("books_published").clear()

                    for book in publisher.books_published:
                        book_element = ET.SubElement(publisher_element.find("books_published"), "book")
                        ET.SubElement(book_element, "title").text = book.title
                        ET.SubElement(book_element, "author").text = book.author
                        ET.SubElement(book_element, "price").text = str(book.price)
                        ET.SubElement(book_element, "quantity").text = str(book.quantity)

                    tree.write(self.filepath)
                    return True

            raise PublisherNotFoundError(f"Publisher '{publisher.name}' not found for update.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except PublisherNotFoundError as e:
            print(e)
            return False

    def delete(self, name: str) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for publisher_element in root.findall("publisher"):
                if publisher_element.find("name").text == name:
                    root.remove(publisher_element)
                    tree.write(self.filepath)
                    return True
            raise PublisherNotFoundError(f"Publisher '{name}' not found for deletion.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except PublisherNotFoundError as e:
            print(e)
            return False
