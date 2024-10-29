import xml.etree.ElementTree as ET
from Publisher import Publisher
from Book import Book

class PublisherXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, publisher: Publisher):
        try:
            root = ET.Element("publishers")
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
        except Exception as e:
            print(f"Error creating XML: {e}")

    def read(self, name: str) -> Publisher:
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
            print(f"Publisher '{name}' not found.")
            return None
        except Exception as e:
            print(f"Error reading XML: {e}")
            return None

    def update(self, publisher: Publisher):
        try:
            root = ET.Element("publishers")
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
        except Exception as e:
            print(f"Error updating XML: {e}")

    def delete(self, name: str):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for publisher_element in root.findall("publisher"):
                if publisher_element.find("name").text == name:
                    root.remove(publisher_element)
                    tree.write(self.filepath)
                    return True
            print(f"Publisher '{name}' not found for deletion.")
            return False
        except Exception as e:
            print(f"Error deleting XML: {e}")
            return False
