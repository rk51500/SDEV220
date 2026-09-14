class Customer:
    def __init__(self, name, phone, order_type):
        self.name = name
        self.phone = phone
        self.order_type = order_type

    def get_info(self):
        return f"{self.name} | {self.phone} | {self.order_type}"