import json
from typing import Optional, List
from Order import Order
from Book import Book
from Customer import Customer

class OrderJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath
    def create(self, order: Order):
        order_data = {
            "order_id": order.order_id,
            "customer": order.customer.name,
            "status": order.status,
            "books": [{"title": book.title, "price": book.price} for book in order.books],
            "total_amount": order.total_amount
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"orders": []}

        data["orders"].append(order_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, order_id: str, customer: Customer) -> Optional[Order]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for order_data in data.get("orders", []):
                if order_data["order_id"] == order_id:
                    order = Order(order_data["order_id"], customer, order_data["status"])
                    books = [Book(book["title"], book["price"]) for book in order_data["books"]]
                    order.books = books
                    order.calculate_total()
                    return order
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error reading JSON: file not found or invalid format.")
            return None

    def update_status(self, order_id: str, new_status: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for order_data in data.get("orders", []):
                if order_data["order_id"] == order_id:
                    order_data["status"] = new_status
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error updating JSON: file not found or invalid format.")
            return False
        return False

    def delete(self, order_id: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            data["orders"] = [order for order in data.get("orders", []) if order["order_id"] != order_id]
            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error deleting JSON: file not found or invalid format.")
            return False
