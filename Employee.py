
class Employee:
    def __init__(self, name: str, position: str, salary: float):
        self.name = name
        self.position = position
        self.salary = max(salary, 0) # salary >= 0

    def calculate_annual_salary(self) -> float:
        return self.salary * 12

    def __str__(self):
        return (f"Employee(name='{self.name}', position='{self.position}', "
                f"salary={self.salary})")