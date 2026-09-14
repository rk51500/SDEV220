import tkinter as tk
from tkinter import messagebox

from customer import Customer
from order import Order
from inventory import InventoryManager


class TamaleTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tamale Tracker")
        self.root.geometry("500x600")

        self.inventory = InventoryManager()
        self.orders = []

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Tamale Tracker", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.root, text="Customer Name").pack()
        self.name_entry = tk.Entry(self.root, width=40)
        self.name_entry.pack()

        tk.Label(self.root, text="Phone Number").pack()
        self.phone_entry = tk.Entry(self.root, width=40)
        self.phone_entry.pack()

        tk.Label(self.root, text="Order Type").pack()
        self.order_type_var = tk.StringVar(value="Pickup")
        tk.OptionMenu(self.root, self.order_type_var, "Pickup", "Delivery").pack()

        tk.Label(self.root, text="Tamale Flavor").pack()
        self.product_var = tk.StringVar(value="Pork")
        tk.OptionMenu(self.root, self.product_var, *self.inventory.get_product_names()).pack()

        tk.Label(self.root, text="Quantity").pack()
        self.quantity_entry = tk.Entry(self.root, width=20)
        self.quantity_entry.pack()

        tk.Button(self.root, text="Place Order", command=self.place_order).pack(pady=10)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory).pack(pady=5)
        tk.Button(self.root, text="Clear", command=self.clear_form).pack(pady=5)

        self.output_box = tk.Text(self.root, height=15, width=55)
        self.output_box.pack(pady=10)

    def place_order(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        order_type = self.order_type_var.get()
        product_name = self.product_var.get()

        try:
            quantity = int(self.quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        if name == "" or phone == "":
            messagebox.showerror("Error", "Please enter customer name and phone number.")
            return

        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be greater than zero.")
            return

        customer = Customer(name, phone, order_type)
        order = Order(customer)
        product = self.inventory.get_product(product_name)

        if order.add_item(product, quantity):
            self.orders.append(order)
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, order.get_summary())
        else:
            messagebox.showerror("Error", "Not enough inventory available.")

    def view_inventory(self):
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, self.inventory.get_inventory_summary())

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.output_box.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = TamaleTrackerApp(root)
    root.mainloop()