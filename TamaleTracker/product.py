class TamaleProduct:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def reduce_stock(self, amount):
        if amount <= self.quantity:
            self.quantity -= amount
            return True
        return False

    def restock(self, amount):
        self.quantity += amount