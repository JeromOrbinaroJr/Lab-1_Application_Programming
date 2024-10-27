
class Employee:
    def __init__(self, name: str, position: str, salary: float):
        try:
            assert isinstance(name, str) and name, "Name name must be a non-empty string"
            assert isinstance(position, str) and position, "Position name must be a non-empty string"
            assert isinstance(salary, (int, float)) and salary >= 0, "Salary must be a non-negative number."

            self.name = name
            self.position = position
            self.salary = salary

        except AssertionError as e:
            print(f"Initialization Error: {e}")

    def calculate_annual_salary(self) -> float:
        try:
            return self.salary * 12
        except Exception as e:
            print(f"Error calculating annual salary: {e}")
            return 0.0

    def __str__(self):
        return (f"Employee(name='{self.name}', position='{self.position}', "
                f"salary={self.salary})")