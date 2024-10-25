from typing import Optional

class Book:
    def __init__(self, title: str, author: Optional['Author'], price: float, quantity: int):
        self.title = title
        self.author = author
        self.price = max(price, 0)  # price >= 0
        self.quantity = max(quantity, 0)  # quantity >= 0

    def update_quantity(self, new_quantity: int):
        if new_quantity >= 0:
            self.quantity = new_quantity
        else:
            raise ValueError("Quantity cannot be negative.")

    def apply_discount(self, discount_percent: int):
        if (discount_percent >= 0) and (discount_percent <= 100):
            new_price = self.price - (self.price * (discount_percent / 100))
            self.price = max(new_price, 0)  # new_price >= 0
        else:
            raise ValueError("Discount percent cannot be negative.")

    def __str__(self):
        author_name = self.author.name if self.author else "Unknown"
        return (
            f"Book(title={self.title}, author={author_name}, price={self.price}, quantity={self.quantity})"
        )
