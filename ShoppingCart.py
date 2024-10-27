from typing import List
from Book import Book

class ShoppingCart:
    def __init__(self):
        self.items: List[Book] = []
        self.total_price = 0.0

    def add_item(self, book: Book, quantity: int = 1):
        try:
            assert isinstance(book, Book), "The item must be an instance of Book."
            assert isinstance(quantity, int) and quantity > 0, "Quantity must be a positive integer."

            if book.quantity >= quantity:
                self.items.extend([book] * quantity)
                book.update_quantity(book.quantity - quantity)
                self.calculate_total()
            else:
                raise ValueError(f"Not enough copies of '{book.title}' available.")

        except AssertionError as e:
            print(f"Assertion error in add_item: {e}")
        except ValueError as e:
            print(f"Value error in add_item: {e}")
        except Exception as e:
            print(f"Unexpected error in add_item: {e}")

    def remove_item(self, title: str):
        try:
            assert isinstance(title, str) and title, "Title must be a non-empty string."

            self.items = [item for item in self.items if item.title != title]
            self.calculate_total()

        except AssertionError as e:
            print(f"Assertion error in remove_item: {e}")
        except Exception as e:
            print(f"Unexpected error in remove_item: {e}")

    def calculate_total(self):
        try:
            self.total_price = sum(book.price for book in self.items)

        except Exception as e:
            print(f"Unexpected error in calculate_total: {e}")
