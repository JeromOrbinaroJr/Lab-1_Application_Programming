from typing import List
from Book import Book
from Customer import Customer
from Employee import Employee
from Order import Order
from Inventory import Inventory


class Bookstore:
    def __init__(self, name: str, location: str):
        try:
            assert isinstance(name, str) and name, "Name must be a non-empty string."
            assert isinstance(location, str) and location, "Location must be a non-empty string."

            self.name = name
            self.location = location
            self.inventory = Inventory()
            self.employees: List[Employee] = []
            self.customers: List[Customer] = []
            self.orders: List[Order] = []

        except AssertionError as e:
            print(f"Error initializing Bookstore: {e}")
        except Exception as e:
            print(f"Unexpected error initializing Bookstore: {e}")

    def add_book(self, book: Book):
        try:
            assert isinstance(book, Book), "The book must be an instance of Book."
            self.inventory.add_book(book)

        except AssertionError as e:
            print(f"Error in add_book: {e}")
        except Exception as e:
            print(f"Unexpected error in add_book: {e}")

    def remove_book(self, title: str):
        try:
            assert isinstance(title, str) and title, "Title must be a non-empty string."
            self.inventory.remove_book(title)

        except AssertionError as e:
            print(f"Error in remove_book: {e}")
        except Exception as e:
            print(f"Unexpected error in remove_book: {e}")

    def find_book_by_title(self, title: str):
        try:
            assert isinstance(title, str) and title, "Title must be a non-empty string."
            return self.inventory.find_book_by_title(title)

        except AssertionError as e:
            print(f"Error in find_book_by_title: {e}")
        except Exception as e:
            print(f"Unexpected error in find_book_by_title: {e}")
            return None

    def list_books(self):
        try:
            return self.inventory.list_books()

        except Exception as e:
            print(f"Unexpected error in list_books: {e}")
            return []

    def register_customer(self, customer: Customer):
        try:
            assert isinstance(customer, Customer), "Customer must be an instance of Customer."
            self.customers.append(customer)

        except AssertionError as e:
            print(f"Error in register_customer: {e}")
        except Exception as e:
            print(f"Unexpected error in register_customer: {e}")

    def process_order(self, order: Order):
        try:
            assert isinstance(order, Order), "Order must be an instance of Order."
            order.calculate_total()
            self.orders.append(order)

        except AssertionError as e:
            print(f"Error in process_order: {e}")
        except Exception as e:
            print(f"Unexpected error in process_order: {e}")
