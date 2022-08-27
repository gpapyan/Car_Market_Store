import shelve
from tabulate import tabulate


class Cars:
    def __init__(self, sku, model,
                 price, year, is_available):
        self.sku = sku
        self.model = model
        self.price = price
        self.year = year
        self.is_available = is_available

    def __repr__(self):
        with shelve.open("cars.db", writeback=True) as db_cars:
            table = []
            headers = ['Car SKU', 'MODEL',
                       'Price', 'Car Year', 'Status']
            for crs in db_cars.values():
                table.append([crs.sku, crs.model,
                              crs.price, crs.year, crs.is_available])

        return tabulate(table, headers, tablefmt="fancy_grid",
                        stralign="left", numalign="left")
