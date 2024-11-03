import xml.etree.ElementTree as ET
from typing import Optional
from Customer import Customer
from Order import Order

class CustomerExistsError(Exception):
    pass

class CustomerNotFoundError(Exception):
    pass

class CustomerXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, customer: Customer):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("customers")

        for customer_element in root.findall("customer"):
            if customer_element.find("name").text == customer.name:
                raise CustomerExistsError(f"Customer '{customer.name}' already exists.")

        customer_element = ET.SubElement(root, "customer")
        ET.SubElement(customer_element, "name").text = customer.name
        ET.SubElement(customer_element, "email").text = customer.email

        purchase_history = ET.SubElement(customer_element, "purchase_history")
        for order in customer.purchase_history:
            order_element = ET.SubElement(purchase_history, "order", id=order.order_id)
            ET.SubElement(order_element, "status").text = order.status
            ET.SubElement(order_element, "total_amount").text = str(order.total_amount)

        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def read(self, name: str) -> Optional[Customer]:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for customer_element in root.findall("customer"):
                if customer_element.find("name").text == name:
                    email = customer_element.find("email").text
                    customer = Customer(name, email)

                    purchase_history_element = customer_element.find("purchase_history")
                    for order_element in purchase_history_element.findall("order"):
                        order_id = order_element.get("id")
                        status = order_element.find("status").text
                        total_amount = float(order_element.find("total_amount").text)
                        order = Order(order_id, customer, status)
                        order.total_amount = total_amount
                        customer.add_to_purchase_history(order)
                    return customer
            raise CustomerNotFoundError(f"Customer '{name}' not found.")
        except (FileNotFoundError, ET.ParseError):
            return None

    def update_email(self, name: str, new_email: str) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for customer_element in root.findall("customer"):
                if customer_element.find("name").text == name:
                    customer_element.find("email").text = new_email
                    tree.write(self.filepath)
                    return True
            raise CustomerNotFoundError(f"Customer '{name}' not found for update.")
        except (FileNotFoundError, ET.ParseError):
            return False

    def delete(self, name: str) -> bool:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            for customer_element in root.findall("customer"):
                if customer_element.find("name").text == name:
                    root.remove(customer_element)
                    tree.write(self.filepath)
                    return True
            raise CustomerNotFoundError(f"Customer '{name}' not found for deletion.")
        except (FileNotFoundError, ET.ParseError):
            return False
