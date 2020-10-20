from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton


class MainApp(MDApp):
    def build(self):
        return MDIconButton(icon = 'images/countries/Austria.png')


if __name__ == '__main__':
    MainApp().run()