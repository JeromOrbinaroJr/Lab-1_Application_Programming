import xml.etree.ElementTree as ET
from typing import Optional, List
from Order import Order
from Book import Book
from Customer import Customer

class OrderExistsError(Exception):
    pass

class OrderNotFoundError(Exception):
    pass


class OrderXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, order: Order):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("orders")

        for order_element in root.findall("order"):
            if order_element.get("id") == order.order_id:
                raise OrderExistsError(f"Order '{order.order_id}' already exists.")

        order_element = ET.SubElement(root, "order", id=order.order_id)
        ET.SubElement(order_element, "customer").text = order.customer.name
        ET.SubElement(order_element, "status").text = order.status

        books_element = ET.SubElement(order_element, "books")
        for book in order.books:
            book_element = ET.SubElement(books_element, "book", title=book.title)
            ET.SubElement(book_element, "price").text = str(book.price)

        ET.SubElement(order_element, "total_amount").text = str(order.total_amount)

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, order_id: str, customer: Customer) -> Optional[Order]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for order_element in root.findall("order"):
                if order_element.get("id") == order_id:
                    status = order_element.find("status").text
                    books = [
                        Book(book.get("title"), float(book.find("price").text))
                        for book in order_element.find("books").findall("book")
                    ]
                    order = Order(order_id, customer, status)
                    order.books = books
                    order.calculate_total()
                    return order
        except (FileNotFoundError, ET.ParseError):
            return None
        return None

    def update_status(self, order_id: str, new_status: str) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for order_element in root.findall("order"):
                if order_element.get("id") == order_id:
                    order_element.find("status").text = new_status
                    tree.write(self.filepath)
                    return True
            raise OrderNotFoundError(f"Order '{order_id}' not found for update.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except OrderNotFoundError as e:
            print(e)
            return False

    def delete(self, order_id: str) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for order_element in root.findall("order"):
                if order_element.get("id") == order_id:
                    root.remove(order_element)
                    tree.write(self.filepath)
                    return True
            raise OrderNotFoundError(f"Order '{order_id}' not found for deletion.")
        except (FileNotFoundError, ET.ParseError):
            return False
        except OrderNotFoundError as e:
            print(e)
            return False
