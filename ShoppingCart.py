from typing import List, Dict
from Book import Book


class ShoppingCart:
    def __init__(self):
        self.items: Dict[Book, int] = {}
        self.total_price = 0.0

    def add_item(self, book: Book, quantity: int = 1):
        try:
            assert isinstance(book, Book), "The item must be an instance of Book."
            assert isinstance(quantity, int) and quantity > 0, "Quantity must be a positive integer."

            if book.quantity >= quantity:
                if book in self.items:
                    self.items[book] += quantity
                else:
                    self.items[book] = quantity

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

    def remove_item(self, book: Book, quantity: int = 1):
        try:
            assert isinstance(book, Book), "The item must be an instance of Book."
            assert isinstance(quantity, int) and quantity > 0, "Quantity must be a positive integer."

            if book in self.items:
                if self.items[book] > quantity:
                    self.items[book] -= quantity
                    book.update_quantity(book.quantity + quantity)
                elif self.items[book] == quantity:
                    del self.items[book]
                    book.update_quantity(book.quantity + quantity)
                else:
                    raise ValueError(
                        f"Cannot remove {quantity} copies of '{book.title}', only {self.items[book]} available in cart.")

                self.calculate_total()
            else:
                raise ValueError(f"The book '{book.title}' is not in the shopping cart.")

        except AssertionError as e:
            print(f"Assertion error in remove_item: {e}")
        except ValueError as e:
            print(f"Value error in remove_item: {e}")
        except Exception as e:
            print(f"Unexpected error in remove_item: {e}")

    def calculate_total(self):
        try:
            self.total_price = sum(book.price * quantity for book, quantity in self.items.items())
        except Exception as e:
            print(f"Unexpected error in calculate_total: {e}")

    def clear_cart(self):
        try:
            for book, quantity in self.items.items():
                book.update_quantity(book.quantity + quantity)
            self.items.clear()
            self.total_price = 0.0
        except Exception as e:
            print(f"Unexpected error in clear_cart: {e}")

    def __str__(self):
        cart_contents = ", ".join([f"{book.title} (x{quantity})" for book, quantity in self.items.items()])
        return f"ShoppingCart(items=[{cart_contents}], total_price={self.total_price:.2f})"
