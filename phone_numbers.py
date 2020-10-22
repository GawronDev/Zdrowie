from kivymd.uix.list import MDList, IconLeftWidget, OneLineIconListItem, IconRightWidget, OneLineAvatarIconListItem, \
    ThreeLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.gridlayout import MDGridLayout
import pickle


class SecondScreen(MDGridLayout):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.adaptive_height = True
        self.cols = 1
        self.id = 'numbers_container'


class PhoneContent(MDBoxLayout):
    def __init__(self, content, **kwargs):
        super(PhoneContent, self).__init__(**kwargs)
        self.adaptive_height = True
        item = OneLineIconListItem(text=content)
        icon = IconLeftWidget(icon='phone')
        self.add_widget(item)
        item.add_widget(icon)


class ProvinceContent(MDList):
    def __init__(self, content, **kwargs):
        super(ProvinceContent, self).__init__(**kwargs)
        self.cols = 1
        self.adaptive_height = True
        for i in content:
            numbers = i[2] + '     ' + i[3]
            self.add_widget(ThreeLineListItem(text=i[0],
                                              secondary_text=i[1],
                                              tertiary_text=numbers))


class CountryOneLineIconListItem(OneLineIconListItem):
    pass


class Show(MDList):
    NORMAL = 4
    EXTENDED = 16

    def __init__(self, **kwargs):
        super(Show, self).__init__(**kwargs)
        self.numbers = self.pickle_list()[3]
        self.countries = []
        self.container = None
        self.prov_item = None
        for self.key, self.value in self.numbers.items():
            icon = IconLeftWidget(icon=f'images/countries/{self.key}.png', size_hint=(0.9, 0.9))
            self.item = CountryOneLineIconListItem(text=str(self.key))
            self.add_widget(self.item)
            self.item.add_widget(icon)

    def down_button(self, country, *args):
        print(country)
        self.phone_number_screen_manager.current = 'phone_number_list'
        numbers = self.pickle_list()[3][country]
        if len(numbers) == self.NORMAL:
            names = self.pickle_list()[0]
            self.container = SecondScreen()
            self.phone_container.add_widget(self.container)
            for i in range(self.NORMAL):
                self.container.add_widget(MDExpansionPanel(icon=f'images/emergency/{names[i]}.png',
                                                           content=PhoneContent(numbers[i]),
                                                           panel_cls=MDExpansionPanelOneLine(text=names[i])))

        elif len(numbers) == self.EXTENDED:
            names = self.pickle_list()[1]
            self.container = SecondScreen()
            self.phone_container.add_widget(self.container)
            self.prov_item = OneLineAvatarIconListItem(text='Numery ws. koronawirusa w Województwach',
                                                  on_release=self.provinces_list)
            prov_item_icon_left = IconLeftWidget(icon='images/emergency/mask.png', size_hint=(0.9, 0.9))
            prov_item_icon_right = IconRightWidget(icon='arrow-right')
            self.phone_list_container.add_widget(self.prov_item)
            self.prov_item.add_widget(prov_item_icon_left)
            self.prov_item.add_widget(prov_item_icon_right)
            for i in range(self.EXTENDED):
                self.container.add_widget(MDExpansionPanel(icon=f'images/emergency/{names[i]}.png',
                                                           content=PhoneContent(numbers[i]),
                                                           panel_cls=MDExpansionPanelOneLine(text=names[i])))

    def provinces_list(self, *args):
        self.phone_number_screen_manager.current = 'phone_provinces'
        content = self.pickle_list()[4]
        for key, value in content.items():
            item = MDExpansionPanel(icon=f'images/provinces/{key}.png',
                                    content=ProvinceContent(content[key]),
                                    panel_cls=MDExpansionPanelOneLine(text=key))

            self.phone_provinces.add_widget(item)

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

    def clear_screen(self):
        self.phone_container.remove_widget(self.container)

    def clear_provinces(self):
        self.phone_list_container.remove_widget(self.prov_item)