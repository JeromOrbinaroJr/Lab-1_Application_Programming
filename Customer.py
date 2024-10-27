from typing import List
from Order import Order

class Customer:
    def __init__(self, name: str, email: str):
        try:
            assert isinstance(name, str) and name, "Name must be a non-empty string"
            assert isinstance(email, str) and email, "Email name must be a non-empty string"

            self.name = name
            self.email = email
            self.purchase_history: List[Order] = []
        except AssertionError as e:
            print(f"Initialization Error: {e}")

    def add_to_purchase_history(self, order: Order):
        try:
            if not isinstance(order, Order):
                raise TypeError("Expected an instance of Order.")
            self.purchase_history.append(order)
        except TypeError as e:
            print(f"Add to Purchase History Error: {e}")

    def get_purchase_history(self):
        try:
            if not self.purchase_history:
                raise ValueError("No purchase history available.")
            return [str(order) for order in self.purchase_history]
        except ValueError as e:
            print(f"Get Purchase History Error: {e}")
            return []
