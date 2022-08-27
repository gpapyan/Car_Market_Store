from person import Persons
import shelve
from tabulate import tabulate


class Buyer(Persons):
    def __init__(self, p_id, name, surname, city, card_name, budget):
        super().__init__(p_id, name, surname, city, card_name)
        self.budget = budget
        # self.spent_money = spent_money
        # self.buy_car = buy_car

    def __repr__(self):
        with shelve.open("buyers.db", writeback=True) as db_buyers:
            table = []
            headers = ['Bought Car', 'Buyer ID', 'budget', 'Spent Money']
            for bc in db_buyers.values():
                table.append([bc.buy_car, bc.p_id,
                              bc.budget, bc.spent_money])

        return tabulate(table, headers, tablefmt="fancy_grid",
                        stralign="left", numalign="right")
