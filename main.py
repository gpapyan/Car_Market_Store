from car_market import CarMarket

if __name__ == '__main__':
    crs = CarMarket()
    while True:
        print(crs.show_menu())
        print(crs.menu())
