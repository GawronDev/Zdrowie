from kivy.uix.gridlayout import GridLayout
from kivymd.uix.picker import MDThemePicker


class Ustawienia(GridLayout):
    """Klasa ustawień"""

    def open_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    def back_to_home_screen(self):
        self.nav_drawer.set_state('closed')
        self.main_screen_manager.current = "main_screen"

    def back_to_settings(self):
        self.main_screen_manager.current = "settings"

