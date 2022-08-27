import shelve
import datetime
from tabulate import tabulate
from cars import Cars
from seller import Seller
from buyer import Buyer


class CarMarket:
    def __init__(self):
        self.db_cars = shelve.open("cars.db", writeback=True)  # books = cars
        self.db_sold = shelve.open("sold.db", writeback=True)  # rental = seller
        self.db_buyers = shelve.open("buyers.db", writeback=True)  # client = buyers

    def add_cars(self):
        sku = input("Car SKU: ")
        model = input("MODEL: ")
        price = int(input("Price: "))
        year = input("Car Year: ")
        cars = Cars(sku, model,
                    price, year, is_available="available")
        self.db_cars[cars.sku] = cars
        return "Car was successfully added."

    def search_cars(self):
        model = input("Enter Car Model: ")
        count = 0
        for crs in self.db_cars.values():
            if model == crs.model:
                count += 1

        if count == 0:
            print(f'No car found with "{model}" model!')
        else:
            print(f'Found {count} car(s) with "{model}" model!')

        park = []
        headers = ['Car SKU', 'MODEL',
                   'Price', 'Car Year', 'Status']
        for crs in self.db_cars.values():
            if model == crs.model:
                park.append([crs.sku, model,
                             crs.price, crs.year, crs.is_available])

        return tabulate(park, headers, tablefmt="fancy_grid",
                        stralign="left", numalign="left")

    def delete_cars(self):
        sku = input("Enter Car SKU: ")
        if sku in self.db_cars:
            del self.db_cars[sku]
            return "Car was successfully deleted."
        else:
            return "Sorry, to delete doesn't exist" \
                   " in the car park!"

    def member_card(self, card_name):
        print("You don't have a Member Card. "
              "Please input the following information.")
        name = input('Enter Name: ')
        surname = input('Enter Surname: ')
        city = input('Enter City: ')
        budget = int(input('Enter Budget: '))
        p_id = len(self.db_buyers.keys()) + 1
        buyer = Buyer(p_id, name, surname, budget, city, card_name)
        self.db_buyers[f'{len(self.db_buyers.keys()) + 1}'] = buyer
        print("Your Member Card was opened successfully)")
        return buyer.p_id

    def sold_cars(self):
        card_name = input("Enter Member Card: ")
        for mc in self.db_buyers.values():
            if card_name == mc.card_name:
                p_id = mc.p_id
                break
        else:
            p_id = self.member_card(card_name)

        model = input("Enter Car Model: ")
        for crs in self.db_cars.values():
            if model == crs.model and crs.is_available == "available":
                budget = 155000
                if budget >= crs.price:
                    money = 0
                    money += crs.price
                    new_budget = budget - crs.price
                    spent_money = budget - new_budget
                    self.db_sold[crs.sku] = \
                        Seller(crs.sku, p_id, crs.price,
                               datetime.datetime.now())
                    # self.db_buyers[crs.sku] = \
                    #     Buyer(crs.sku, p_id, new_budget,
                    #           spent_money)
                    self.db_cars[crs.sku] = \
                        Cars(crs.sku, model,
                             crs.price, crs.year, "Not Available")
                    print('Your checkout was successfully implemented.')
                    break
                else:
                    return "You Dont Have Enough Money"
        else:
            return "This car is not available now."

    def return_car(self):
        sku = input('Enter SKU: ')
        if sku in self.db_sold.keys():
            self.db_cars[sku].is_available = "available"
            del self.db_sold[sku]
            return 'Your return was successfully implemented.'
        else:
            return "Please input a valid car sku!"

    def search_sold_car(self):
        sku = input("Enter Sold Car SKU: ")
        count = 0
        if sku in self.db_sold.keys():
            table = []
            headers = ['Sold Car', 'Seller ID', 'Money', 'Sold Date']
            table.append([sku,
                          self.db_sold[sku].p_id,
                          self.db_sold[sku].money])
            return tabulate(table, headers, tablefmt="fancy_grid",
                            stralign="left", numalign="left")
        else:
            return f'No Car found with "{sku}" SKU!'

    def exit_func(self):
        self.db_cars.close()
        self.db_sold.close()
        self.db_buyers.close()
        return exit()

    def show_menu(self):
        return ("ac   - Add New Car\n"
                "sc   - Search Car\n"
                "dc   - Delete a Car\n"
                "sold - Sold Car\n"
                "ssc - Search Sold Car\n"
                "return - Return Sold Car\n"
                "x   - Exit")

    def menu(self):
        all_actions = {
            "ac": self.add_cars,
            "sc": self.search_cars,
            "dc": self.delete_cars,
            "sold": self.sold_cars,
            "ssc": self.search_sold_car,
            "return": self.return_car,
            "x": self.exit_func}

        return all_actions.get(input("Please choose one of the these actions: "), lambda: "Invalid input!")()

