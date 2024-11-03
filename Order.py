from typing import List
from Book import Book
from Customer import Customer

class Order:
    def __init__(self, order_id: str, customer: Customer, status: str = "Pending"):
        try:
            assert isinstance(order_id, str) and order_id, "Order ID must be a non-empty string"
            assert isinstance(customer, Customer), "Customer must be an instance of Customer"
            valid_statuses = ["Pending", "Shipped", "Delivered", "Canceled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid initial status '{status}'. Valid statuses are: {valid_statuses}")

            self.order_id = order_id
            self.customer = customer
            self.books: List[Book] = []
            self.total_amount = 0.0
            self.status = status
        except (AssertionError, ValueError) as e:
            print(f"Error initializing order: {e}")

    def add_book(self, book: Book, quantity: int = 1):
        try:
            if not isinstance(book, Book):
                raise TypeError("Expected an instance of Book.")
            if not isinstance(quantity, int) or quantity <= 0:
                raise ValueError("Quantity must be a positive integer.")

            if book.quantity >= quantity:
                self.books.extend([book] * quantity)
                book.update_quantity(book.quantity - quantity)
                self.calculate_total()
            else:
                raise ValueError(f"Not enough copies of '{book.title}' available.")
        except (TypeError, ValueError) as e:
            print(f"Error adding book to order: {e}")

    def calculate_total(self):
        try:
            self.total_amount = sum(book.price for book in self.books)
        except Exception as e:
            print(f"Error calculating total amount: {e}")

    def update_status(self, new_status: str):
        try:
            valid_statuses = ["Pending", "Shipped", "Delivered", "Canceled"]
            if new_status not in valid_statuses:
                raise ValueError(f"Invalid status '{new_status}'. Valid statuses are: {valid_statuses}")
            self.status = new_status
        except ValueError as e:
            print(f"Error updating order status: {e}")

    def __str__(self):
        book_titles = [book.title for book in self.books]
        return (
            f"Order(order_id={self.order_id}, customer={self.customer.name}, "
            f"books={book_titles}, total_amount={self.total_amount}, status={self.status})"
        )
