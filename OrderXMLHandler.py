import xml.etree.ElementTree as ET
from typing import Optional, List
from Order import Order
from Book import Book
from Customer import Customer

class OrderXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, order: Order):
        try:
            root = ET.Element("orders")
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
        except Exception as e:
            print(f"Error creating XML: {e}")

    def read(self, order_id: str, customer: Customer) -> Optional[Order]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for order_element in root.findall("order"):
                if order_element.get("id") == order_id:
                    status = order_element.find("status").text
                    books = []
                    for book_element in order_element.find("books").findall("book"):
                        title = book_element.get("title")
                        price = float(book_element.find("price").text)
                        books.append(Book(title, price))
                    order = Order(order_id, customer, status)
                    order.books = books
                    order.calculate_total()
                    return order
            return None
        except Exception as e:
            print(f"Error reading XML: {e}")
            return None

    def update_status(self, order_id: str, new_status: str):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for order_element in root.findall("order"):
                if order_element.get("id") == order_id:
                    order_element.find("status").text = new_status
                    tree.write(self.filepath)
                    return True
            return False
        except Exception as e:
            print(f"Error updating XML: {e}")
            return False

    def delete(self, order_id: str):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for order_element in root.findall("order"):
                if order_element.get("id") == order_id:
                    root.remove(order_element)
                    tree.write(self.filepath)
                    return True
            return False
        except Exception as e:
            print(f"Error deleting XML: {e}")
            return False
