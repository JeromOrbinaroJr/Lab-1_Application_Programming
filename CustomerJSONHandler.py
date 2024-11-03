import json
from typing import Optional
from Customer import Customer
from Order import Order

class CustomerExistsError(Exception):
    pass

class CustomerNotFoundError(Exception):
    pass

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

        for existing_customer in data.get("customers", []):
            if existing_customer["name"] == customer.name:
                raise CustomerExistsError(f"Customer '{customer.name}' already exists.")

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
            raise CustomerNotFoundError(f"Customer '{name}' not found.")
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update_email(self, name: str, new_email: str) -> bool:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for customer_data in data.get("customers", []):
                if customer_data["name"] == name:
                    customer_data["email"] = new_email
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
            raise CustomerNotFoundError(f"Customer '{name}' not found for update.")
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def delete(self, name: str) -> bool:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("customers", []))
            data["customers"] = [cust for cust in data.get("customers", []) if cust["name"] != name]

            if len(data["customers"]) == original_length:
                raise CustomerNotFoundError(f"Customer '{name}' not found for deletion.")

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
