from product import TamaleProduct


class InventoryManager:
    def __init__(self):
        self.products = {
            "Pork": TamaleProduct("Pork", 2.50, 100),
            "Chicken": TamaleProduct("Chicken", 2.50, 100),
            "Cheese": TamaleProduct("Cheese", 2.75, 80),
            "Sweet": TamaleProduct("Sweet", 3.00, 60)
        }

    def get_product(self, name):
        return self.products.get(name)

    def get_product_names(self):
        return list(self.products.keys())

    def get_inventory_summary(self):
        summary = "Current Inventory:\n"
        for product in self.products.values():
            summary += f"{product.name}: {product.quantity} available\n"
        return summary