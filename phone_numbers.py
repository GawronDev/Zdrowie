from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import IconLeftWidget
from kivy.properties import StringProperty


class CountrySelect(OneLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super(CountrySelect, self).__init__(**kwargs)


class CountryWidget(IconLeftWidget):
    def __init__(self, **kwargs):
        super(CountryWidget, self).__init__(**kwargs)
        self.icon = 'images/countries/Polska.png'


class Show():
    def __init__(self):
        self.icon = 'images/countries/Austria.png'