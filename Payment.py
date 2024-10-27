class Payment:
    def __init__(self, amount: float, status: str = "Pending"):
        try:
            assert isinstance(amount, (int, float)) and amount >= 0, "Amount must be a non-negative number"
            valid_statuses = ["Pending", "Completed", "Failed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid initial status '{status}'. Valid statuses are: {valid_statuses}")

            self.amount = amount
            self.status = status
        except (AssertionError, ValueError) as e:
            print(f"Error initializing payment: {e}")

    def process_payment(self):
        try:
            if self.amount > 0:
                self.status = "Completed"
            else:
                raise ValueError("Payment amount must be greater than zero to complete the payment.")
        except ValueError as e:
            print(f"Error processing payment: {e}")
            self.status = "Failed"
