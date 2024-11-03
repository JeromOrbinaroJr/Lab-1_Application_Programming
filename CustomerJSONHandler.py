import json
from typing import Optional
from Customer import Customer
from Order import Order

class CustomerJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, customer: Customer):
        customer_data = {
            "name": customer.name,
            "email": customer.email,
            "purchase_history": [
                {"order_id": order.order_id, "status": order.status, "total_amount": order.total_amount}
                for order in customer.purchase_history
            ]
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"customers": []}

        data["customers"].append(customer_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, name: str) -> Optional[Customer]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for customer_data in data.get("customers", []):
                if customer_data["name"] == name:
                    customer = Customer(customer_data["name"], customer_data["email"])
                    for order_data in customer_data["purchase_history"]:
                        order = Order(order_data["order_id"], customer, order_data["status"])
                        order.total_amount = order_data["total_amount"]
                        customer.add_to_purchase_history(order)
                    return customer
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error reading JSON: file not found or invalid format.")
            return None

    def update_email(self, name: str, new_email: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for customer_data in data.get("customers", []):
                if customer_data["name"] == name:
                    customer_data["email"] = new_email
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error updating JSON: file not found or invalid format.")
            return False
        return False

    def delete(self, name: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            data["customers"] = [cust for cust in data.get("customers", []) if cust["name"] != name]
            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error deleting JSON: file not found or invalid format.")
            return False