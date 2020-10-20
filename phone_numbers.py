from kivymd.uix.list import MDList
from kivy.clock import Clock
from kivymd.uix.list import OneLineListItem



class Show(MDList):
    def __init__(self, **kwargs):
        super(Show, self).__init__(**kwargs)

        Clock.schedule_once(self.widgets, 1)

    def widgets(self, *args):
        item = OneLineListItem(text='Austria')
        self.add_widget(item)


