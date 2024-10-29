import json
from typing import Optional
from Employee import Employee

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
            print(f"Error reading JSON: file not found or invalid format.")
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
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error updating JSON: file not found or invalid format.")
            return False
        return False

    def delete(self, name: str):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            data["employees"] = [emp for emp in data.get("employees", []) if emp["name"] != name]
            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error deleting JSON: file not found or invalid format.")
            return False