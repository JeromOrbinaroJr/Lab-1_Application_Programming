import json
from typing import Optional
from Employee import Employee

class EmployeeExistsError(Exception):
    pass

class EmployeeNotFoundError(Exception):
    pass

class EmployeeJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, employee: Employee):
        employee_data = {
            "name": employee.name,
            "position": employee.position,
            "salary": employee.salary
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"employees": []}

        for existing_employee in data.get("employees", []):
            if existing_employee["name"] == employee.name:
                raise EmployeeExistsError(f"Employee '{employee.name}' already exists.")

        data["employees"].append(employee_data)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, name: str) -> Optional[Employee]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for employee_data in data.get("employees", []):
                if employee_data["name"] == name:
                    return Employee(employee_data["name"], employee_data["position"], employee_data["salary"])
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error reading JSON: file not found or invalid format.")
        return None

    def update(self, name: str, new_salary: float):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for employee_data in data.get("employees", []):
                if employee_data["name"] == name:
                    employee_data["salary"] = new_salary
                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
            raise EmployeeNotFoundError(f"Employee '{name}' not found for update.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error updating JSON: file not found or invalid format.")
            return False

    def delete(self, name: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("employees", []))
            data["employees"] = [emp for emp in data.get("employees", []) if emp["name"] != name]

            if len(data["employees"]) == original_length:
                raise EmployeeNotFoundError(f"Employee '{name}' not found for deletion.")

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error deleting JSON: file not found or invalid format.")
            return False
