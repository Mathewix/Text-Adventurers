class Item:
    def __init__(self, name, location, primary, amount, price):
        self.name = name
        self.location = location
        self.primary = primary
        self.amount = amount
        self.price = price

    def info(self):
        print(self.name, self.location, self.primary, self.amount, self.price)
