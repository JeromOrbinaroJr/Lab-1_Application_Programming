from typing import List
from Book import Book
from Customer import Customer
from Employee import Employee
from Order import Order
from Inventory import Inventory

class Bookstore:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.inventory = Inventory()
        self.employees: List[Employee] = []
        self.customers: List[Customer] = []
        self.orders: List[Order] = []

    def add_book(self, book: Book):
        self.inventory.add_book(book)

    def remove_book(self, title: str):
        self.inventory.remove_book(title)

    def find_book_by_title(self, title: str):
        return self.inventory.find_book_by_title(title)

    def list_books(self):
        return self.inventory.list_books()

    def register_customer(self, customer: Customer):
        self.customers.append(customer)

    def process_order(self, order: Order):
        order.calculate_total()
        self.orders.append(order)
