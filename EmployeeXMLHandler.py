import xml.etree.ElementTree as ET
from typing import Optional
from Employee import Employee

class EmployeeExistsError(Exception):
    pass

class EmployeeNotFoundError(Exception):
    pass

class EmployeeXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, employee: Employee):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("employees")

        for employee_element in root.findall("employee"):
            if employee_element.find("name").text == employee.name:
                raise EmployeeExistsError(f"Employee '{employee.name}' already exists.")

        employee_element = ET.SubElement(root, "employee")
        ET.SubElement(employee_element, "name").text = employee.name
        ET.SubElement(employee_element, "position").text = employee.position
        ET.SubElement(employee_element, "salary").text = str(employee.salary)

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, name: str) -> Optional[Employee]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for employee_element in root.findall("employee"):
                if employee_element.find("name").text == name:
                    position = employee_element.find("position").text
                    salary = float(employee_element.find("salary").text)
                    return Employee(name, position, salary)
        except (FileNotFoundError, ET.ParseError):
            print("Error reading XML: file not found or invalid format.")
        return None

    def update(self, name: str, new_salary: float) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for employee_element in root.findall("employee"):
                if employee_element.find("name").text == name:
                    employee_element.find("salary").text = str(new_salary)
                    tree.write(self.filepath)
                    return True

            raise EmployeeNotFoundError(f"Employee '{name}' not found for update.")
        except (FileNotFoundError, ET.ParseError):
            print("Error updating XML: file not found or invalid format.")
            return False

    def delete(self, name: str) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for employee_element in root.findall("employee"):
                if employee_element.find("name").text == name:
                    root.remove(employee_element)
                    tree.write(self.filepath)
                    return True

            raise EmployeeNotFoundError(f"Employee '{name}' not found for deletion.")
        except (FileNotFoundError, ET.ParseError):
            print("Error deleting XML: file not found or invalid format.")
            return False
