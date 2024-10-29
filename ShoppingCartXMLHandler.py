import xml.etree.ElementTree as ET
from ShoppingCart import ShoppingCart
from Book import Book

class ShoppingCartXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, cart: ShoppingCart):
        try:
            root = ET.Element("shopping_cart")
            ET.SubElement(root, "total_price").text = str(cart.total_price)

            items_element = ET.SubElement(root, "items")
            for book, quantity in cart.items.items():
                item_element = ET.SubElement(items_element, "item")
                ET.SubElement(item_element, "title").text = book.title
                ET.SubElement(item_element, "author").text = book.author
                ET.SubElement(item_element, "price").text = str(book.price)
                ET.SubElement(item_element, "quantity").text = str(quantity)

            tree = ET.ElementTree(root)
            tree.write(self.filepath)
        except Exception as e:
            print(f"Error creating XML: {e}")

    def read(self) -> ShoppingCart:
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            cart = ShoppingCart()
            total_price = root.find("total_price").text
            cart.total_price = float(total_price)

            for item_element in root.find("items").findall("item"):
                title = item_element.find("title").text
                author = item_element.find("author").text
                price = float(item_element.find("price").text)
                quantity = int(item_element.find("quantity").text)
                book = Book(title, author, price, quantity)

                cart.add_item(book, quantity)

            return cart
        except Exception as e:
            print(f"Error reading XML: {e}")
            return None

    def update(self, cart: ShoppingCart):
        self.create(cart)

    def delete(self):
        try:
            root = ET.Element("shopping_cart")
            tree = ET.ElementTree(root)
            tree.write(self.filepath)
            return True
        except Exception as e:
            print(f"Error deleting XML: {e}")
            return False
