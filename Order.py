
class Order:
    def __init__(self, order_id, customer, books, total_amount, status):
        self.order_id = order_id
        self.customer = customer
        self.books = books
        self.total_amount = total_amount
        self.status = status

    def calculate_total(self):

    def update_status(self):