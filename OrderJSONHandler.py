import json
from typing import Optional, List
from Order import Order
from Book import Book
from Customer import Customer

class OrderExistsError(Exception):
    pass

class OrderNotFoundError(Exception):
    pass

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

        for existing_order in data.get("orders", []):
            if existing_order["order_id"] == order.order_id:
                raise OrderExistsError(f"Order '{order.order_id}' already exists.")

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
            return None
        return None

    def update_status(self, order_id: str, new_status: str) -> bool:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for order_data in data.get("orders", []):
                if order_data["order_id"] == order_id:
                    order_data["status"] = new_status
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
            raise OrderNotFoundError(f"Order '{order_id}' not found for update.")
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except OrderNotFoundError as e:
            print(e)
            return False

    def delete(self, order_id: str) -> bool:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("orders", []))
            data["orders"] = [order for order in data.get("orders", []) if order["order_id"] != order_id]

            if len(data["orders"]) == original_length:
                raise OrderNotFoundError(f"Order '{order_id}' not found for deletion.")

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except OrderNotFoundError as e:
            print(e)
            return False
