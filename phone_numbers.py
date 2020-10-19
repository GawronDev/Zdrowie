from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import IconLeftWidget
from kivy.properties import StringProperty


class CountrySelect(OneLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super(CountrySelect, self).__init__(**kwargs)
        self.text = '123'


class CountryWidget(IconLeftWidget):
    def __init__(self, **kwargs):
        super(CountryWidget, self).__init__(**kwargs)
        self.icon = 'images/logo16x16.png'
