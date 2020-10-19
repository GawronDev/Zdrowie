from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import IconLeftWidget
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView


class Show(ScrollView):
    def __init__(self):
        super(Show, self).__init__()
        self.icon = 'images/countries/Austria.png'