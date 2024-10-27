class Payment:
    def __init__(self, amount: float, status: str = "Pending"):
        self.amount = amount
        self.status = status

    def process_payment(self):
        if self.amount > 0:
            self.status = "Completed"
        else:
            self.status = "Failed"
