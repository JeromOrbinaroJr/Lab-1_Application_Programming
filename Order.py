from typing import List

from Book import Book
from Customer import Customer

class Order:
    def __init__(self, order_id: str, customer: Customer, total_amount: float, status: str = "Pending"):
        self.order_id = order_id
        self.customer = customer
        self.books: List[Book] = []
        self.total_amount = 0.0
        self.status = status

    def add_book(self, book: Book, quantity: int = 1):
        if book.quantity >= quantity:
            self.books.extend([book] * quantity)
            book.update_quantity(book.quantity-quantity)
            self.calculate_total()
        else:
            raise ValueError(f"Not enough copies of '{book.title}' available.")

    def calculate_total(self):
        self.total_amount = sum(book.price for book in self.books)

    def update_status(self, new_status: str):
        valid_statuses = ["Pending", "Shipped", "Delivered", "Canceled"]
        if new_status in valid_statuses:
            self.status = new_status
        else:
            raise ValueError(f"Invalid status '{new_status}'. Valid statuses: {valid_statuses}")


    def __str__(self):
        book_titles = [book.title for book in self.books]
        return (
            f"Order(order_id={self.order_id}, customer={self.customer.name}, "
            f"books={book_titles}, total_amount={self.total_amount}, status={self.status})"
        )
