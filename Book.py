from typing import Optional

from Author import Author


class Book:
    def __init__(self, title: str, author: Optional['Author'], price: float, quantity: int):
        try:
            assert isinstance(title, str) and title, "Title name must be a non-empty string"
            assert author is None or isinstance(author, Author), "Author must be an instance of Author or None."
            assert isinstance(price, (int, float)) and price >= 0, "Price must be a non-negative number."
            assert isinstance(quantity,int) and quantity >= 0, "Quantity must be a non-negative integer."

            self.title = title
            self.author = author
            self.price = price
            self.quantity = quantity
        except AssertionError as e:
            print(f"Initialization Error: {e}")

    def update_quantity(self, new_quantity: int):
        try:
            if new_quantity >= 0:
                self.quantity = new_quantity
            else:
                raise ValueError("Quantity cannot be negative.")
        except ValueError as e:
            print(f"Quantity Update Error: {e}")

    def apply_discount(self, discount_percent: int):
        try:
            if not (0 <= discount_percent <= 100):
                raise ValueError("Discount percent must be between 0 and 100.")
            new_price = self.price - (self.price * (discount_percent / 100))
            self.price = max(new_price, 0)  # Ensure price doesn't go below zero
        except ValueError as e:
            print(f"Discount Application Error: {e}")

    def __str__(self):
        author_name = self.author.name if self.author else "Unknown"
        return (
            f"Book(title={self.title}, author={author_name}, price={self.price}, quantity={self.quantity})"
        )
