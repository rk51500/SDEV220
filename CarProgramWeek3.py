class Vehicle:
    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type


class Automobile(Vehicle):
    def __init__(self, year, make, model, doors, roof):
        super().__init__("car")
        self.year = year
        self.make = make
        self.model = model
        self.doors = doors
        self.roof = roof


year = input("Enter the year: ")
make = input("Enter the make: ")
model = input("Enter the model: ")
doors = input("Enter the number of doors, 2 or 4: ")
roof = input("Enter the type of roof, solid or sun roof: ")

car = Automobile(year, make, model, doors, roof)

print()
print("Vehicle Information")
print("-------------------")
print(f"Vehicle type: {car.vehicle_type}")
print(f"Year: {car.year}")
print(f"Make: {car.make}")
print(f"Model: {car.model}")
print(f"Number of doors: {car.doors}")
print(f"Type of roof: {car.roof}")