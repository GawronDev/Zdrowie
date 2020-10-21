from kivymd.uix.list import MDList
from kivy.clock import Clock
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
import pickle


class CountryOneLineIconListItem(OneLineIconListItem):
    pass


class Show(MDList):
    def __init__(self, **kwargs):
        super(Show, self).__init__(**kwargs)
        self.numbers = self.pickle_list()[3]
        self.countries = []
        for self.key, self.value in self.numbers.items():
            icon = IconLeftWidget(icon=f'images/countries/{self.key}.png', )
            self.item = CountryOneLineIconListItem(text=str(self.key))
            self.add_widget(self.item)
            self.item.add_widget(icon)
    
    @staticmethod
    def down_button(country):
        print(country)

    @staticmethod
    def pickle_list():
        load = []
        with open('countries_data.dat', 'rb') as file:
            a = pickle.load(file)
            load.append(a)
            b = pickle.load(file)
            load.append(b)
            c = pickle.load(file)
            load.append(c)
            d = pickle.load(file)
            load.append(d)
            e = pickle.load(file)
            load.append(e)
            return load
