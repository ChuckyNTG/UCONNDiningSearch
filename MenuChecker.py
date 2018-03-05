from menuscrap import dining_links, search_menu, dining_menu

class FoodCheck(object):
     
    def __init__(self, time, *args):
        self.foods = [food for food in args]
        self.time = time

    def check_menu(self):
        links = dining_links()
        for val in links.values():
            print search_menu(val, self.foods, self.time)

    def display_menu(self):
        links = dining_links()
        for val in links.values():
            print dining_menu(val)


if __name__=='__main__':
    check = FoodCheck('Dinner','Chicken')       
    check.check_menu()

