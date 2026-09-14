class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []

    def add_item(self, product, quantity):
        if product.reduce_stock(quantity):
            self.items.append((product.name, quantity, product.price))
            return True
        return False

    def calculate_total(self):
        total = 0
        for name, quantity, price in self.items:
            total += quantity * price
        return total

    def get_summary(self):
        summary = f"Customer: {self.customer.get_info()}\n\n"
        summary += "Order Items:\n"

        for name, quantity, price in self.items:
            summary += f"{name}: {quantity} x ${price:.2f} = ${quantity * price:.2f}\n"

        summary += f"\nTotal: ${self.calculate_total():.2f}"
        return summary