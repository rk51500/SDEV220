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
        if amount > 0:
            self.quantity += amount

    def get_display_text(self):
        return f"{self.name} - ${self.price:.2f} ({self.quantity} available)"