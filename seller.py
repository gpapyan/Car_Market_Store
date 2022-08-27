from person import Persons
import shelve
from tabulate import tabulate


class Seller(Persons):
    def __init__(self, money, sold_car, p_id='JS1', name='John', surname='Smith', city='LA'):
        super().__init__(p_id='JS1', name='John', surname='Smith', city='LA', card_name='')
        self.money = money
        self.sold_car = sold_car

    def __repr__(self):
        with shelve.open("sold.db", writeback=True) as db_sold:
            table = []
            headers = ['Sold Car', 'Seller ID', 'Money', 'Sold Date']
            for sc in db_sold.values():
                table.append([sc.sku, sc.p_id,
                              sc.money, sc.datetime.datetime.now()])

        return tabulate(table, headers, tablefmt="fancy_grid",
                        stralign="left", numalign="right")
