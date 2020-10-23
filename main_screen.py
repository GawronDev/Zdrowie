from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from phone_numbers import Show
from main import Zdrowie
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget


class CustomList(OneLineIconListItem):
    def __init__(self, **kwargs):
        super(CustomList, self).__init__(**kwargs)
        self.add_widget(IconLeftWidget(icon='phone'))


class HomePage(MDGridLayout):
    app = Zdrowie()

    def __init__(self,  **kwargs):
        super(HomePage, self).__init__(**kwargs)
        self.cols = 1
        self.cont = MDGridLayout(padding='10dp', cols=1, size_hint_y=0.2*self.size_hint_y)
        self.add_widget(self.cont)
        self.value = 50
        self.bar = MDProgressBar(value=self.value)
        self.lbl1 = MDLabel(text='Liczba:', pos_hint=(1, 1))
        self.cont.add_widget(self.lbl1)
        self.cont.add_widget(self.bar)
        self.twice = MDGridLayout(cols=2)
        self.cont.add_widget(self.twice)
        self.twice.add_widget(MDLabel(text='Śmierci', pos_hint=(0.5, 1)))
        self.twice.add_widget(MDLabel(text='Chroych'))
        app = self.app
        self.data_first = Show.pickle_list(self)[0]
        self.country = 'Polska'
        self.data_second = Show.pickle_list(self)[3][self.country]
        for i in range(len(self.data_first)):
            self.exp = MDExpansionPanel(icon=f'images/emergency/{self.data_first[i]}.png',
                                        content=CustomList(text=self.data_second[i]),
                                        panel_cls=MDExpansionPanelOneLine(
                                            text=self.data_first[i]
                                        ))
            self.add_widget(self.exp)