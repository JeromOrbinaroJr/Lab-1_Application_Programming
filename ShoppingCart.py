from typing import List
from Book import Book

class ShoppingCart:
    def __init__(self):
        self.items: List[Book] = []
        self.total_price = 0.0

    def add_item(self, book: Book, quantity: int = 1):
        if book.quantity >= quantity:
            self.items.extend([book] * quantity)
            book.update_quantity(book.quantity - quantity)
            self.calculate_total()
        else:
            raise ValueError(f"Not enough copies of '{book.title}' available.")

    def remove_item(self, title: str):
        self.items = [item for item in self.items if item.title != title]
        self.calculate_total()

    def calculate_total(self):
        self.total_price = sum(book.price for book in self.items)
