import json
from typing import Optional
from ShoppingCart import ShoppingCart
from Book import Book

class ShoppingCartExistsError(Exception):
    pass

class ShoppingCartNotFoundError(Exception):
    pass

class ShoppingCartJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, cart: ShoppingCart):
        cart_data = {
            "total_price": cart.total_price,
            "items": [
                {
                    "title": book.title,
                    "author": book.author,
                    "price": book.price,
                    "quantity": quantity
                }
                for book, quantity in cart.items.items()
            ]
        }

        try:
            with open(self.filepath, "r") as file:
                existing_data = json.load(file)
                if existing_data:
                    raise ShoppingCartExistsError("Shopping cart already exists.")

            with open(self.filepath, "w") as file:
                json.dump(cart_data, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.filepath, "w") as file:
                json.dump(cart_data, file, indent=4)
        except ShoppingCartExistsError as e:
            print(e)

    def read(self) -> Optional[ShoppingCart]:
        try:
            with open(self.filepath, "r") as file:
                cart_data = json.load(file)

            cart = ShoppingCart()
            cart.total_price = cart_data.get("total_price", 0)

            for item_data in cart_data.get("items", []):
                book = Book(item_data["title"], item_data["author"], item_data["price"], item_data["quantity"])
                cart.add_item(book, item_data["quantity"])

            return cart
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading JSON: {e}")
            return None

    def update(self, cart: ShoppingCart):
        self.create(cart)

    def delete(self):
        try:
            with open(self.filepath, "w") as file:
                json.dump({}, file)
            return True
        except Exception as e:
            print(f"Error deleting JSON: {e}")
            return False
