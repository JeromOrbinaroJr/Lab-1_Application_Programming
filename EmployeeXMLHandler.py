import xml.etree.ElementTree as ET
from typing import Optional
from Employee import Employee

class EmployeeXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, employee: Employee):
        try:
            root = ET.Element("employees")
            employee_element = ET.SubElement(root, "employee")
            ET.SubElement(employee_element, "name").text = employee.name
            ET.SubElement(employee_element, "position").text = employee.position
            ET.SubElement(employee_element, "salary").text = str(employee.salary)

            tree = ET.ElementTree(root)
            tree.write(self.filepath)
        except Exception as e:
            print(f"Error creating XML: {e}")

    def read(self, name: str) -> Optional[Employee]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for employee_element in root.findall("employee"):
                if employee_element.find("name").text == name:
                    position = employee_element.find("position").text
                    salary = float(employee_element.find("salary").text)
                    return Employee(name, position, salary)
            return None
        except Exception as e:
            print(f"Error reading XML: {e}")
            return None

    def update(self, name: str, new_salary: float):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for employee_element in root.findall("employee"):
                if employee_element.find("name").text == name:
                    employee_element.find("salary").text = str(new_salary)
                    tree.write(self.filepath)
                    return True
            return False
        except Exception as e:
            print(f"Error updating XML: {e}")
            return False

    def delete(self, name: str):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for employee_element in root.findall("employee"):
                if employee_element.find("name").text == name:
                    root.remove(employee_element)
                    tree.write(self.filepath)
                    return True
            return False
        except Exception as e:
            print(f"Error deleting XML: {e}")
            return False