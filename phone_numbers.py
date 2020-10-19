from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import IconLeftWidget
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView


class Show(ScrollView):
    def __init__(self, **kwargs):
        super(Show, self).__init__(**kwargs)
