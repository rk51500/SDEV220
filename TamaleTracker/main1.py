from array import array
import tkinter as tk
from tkinter import messagebox

from customer import Customer
from inventory import InventoryManager
from order import Order

from database import create_tables

create_tables()

class TamaleTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tamale Tracker")
        self.root.geometry("620x620")
        self.root.resizable(False, False)

        self.inventory = InventoryManager()
        self.orders = []
        self.daily_totals = array("f")
        self.current_order = None

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Tamale Tracker", font=("Arial", 20, "bold"))
        title.pack(pady=12)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Customer Name").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.name_entry = tk.Entry(form_frame, width=35)
        self.name_entry.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(form_frame, text="Phone Number").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.phone_entry = tk.Entry(form_frame, width=35)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(form_frame, text="Order Type").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.order_type_var = tk.StringVar(value="Pickup")
        tk.OptionMenu(form_frame, self.order_type_var, "Pickup", "Delivery").grid(
            row=2, column=1, sticky="w", padx=5, pady=4
        )

        tk.Label(form_frame, text="Tamale Flavor").grid(row=3, column=0, sticky="w", padx=5, pady=4)
        self.product_var = tk.StringVar(value=self.inventory.get_product_names()[0])
        tk.OptionMenu(form_frame, self.product_var, *self.inventory.get_product_names()).grid(
            row=3, column=1, sticky="w", padx=5, pady=4
        )

        tk.Label(form_frame, text="Quantity").grid(row=4, column=0, sticky="w", padx=5, pady=4)
        self.quantity_entry = tk.Entry(form_frame, width=12)
        self.quantity_entry.grid(row=4, column=1, sticky="w", padx=5, pady=4)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=12)

        tk.Button(button_frame, text="Add Item", width=14, command=self.add_item).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Finish Order", width=14, command=self.finish_order).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="View Inventory", width=14, command=self.view_inventory).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Clear", width=14, command=self.clear_form).grid(row=0, column=3, padx=5)

        self.output_box = tk.Text(self.root, height=22, width=72)
        self.output_box.pack(pady=8)

        self.show_message("Enter customer information, choose a tamale flavor, and add items to begin an order.")

    def add_item(self):
        customer = self.get_customer_from_form()
        if customer is None:
            return

        quantity = self.get_quantity_from_form()
        if quantity is None:
            return

        product_name = self.product_var.get()
        product = self.inventory.get_product(product_name)

        if self.current_order is None:
            self.current_order = Order(customer)

        if self.current_order.add_item(product, quantity):
            self.quantity_entry.delete(0, tk.END)
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, self.current_order.get_summary())
        else:
            messagebox.showerror("Inventory Error", f"Only {product.quantity} {product.name} tamales are available.")

    def finish_order(self):
        if self.current_order is None or len(self.current_order.items) == 0:
            messagebox.showerror("Order Error", "Please add at least one item before finishing the order.")
            return

        self.orders.append(self.current_order)
        self.daily_totals.append(self.current_order.calculate_total())
        summary = self.current_order.get_summary()
        summary += f"\n\nOrder saved. Total orders today: {len(self.orders)}"
        summary += f"\nSales total today: ${sum(self.daily_totals):.2f}"

        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, summary)
        self.current_order = None
        self.clear_customer_fields()

    def view_inventory(self):
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, self.inventory.get_inventory_summary())

    def clear_form(self):
        self.current_order = None
        self.clear_customer_fields()
        self.quantity_entry.delete(0, tk.END)
        self.show_message("Form cleared. Ready for a new order.")

    def clear_customer_fields(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.order_type_var.set("Pickup")

    def get_customer_from_form(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        order_type = self.order_type_var.get()

        if name == "" or phone == "":
            messagebox.showerror("Input Error", "Please enter the customer name and phone number.")
            return None

        return Customer(name, phone, order_type)

    def get_quantity_from_form(self):
        try:
            quantity = int(self.quantity_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a whole number.")
            return None

        if quantity <= 0:
            messagebox.showerror("Input Error", "Quantity must be greater than zero.")
            return None

        return quantity

    def show_message(self, message):
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, message)


if __name__ == "__main__":
    root = tk.Tk()
    app = TamaleTrackerApp(root)
    root.mainloop()
