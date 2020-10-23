from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.picker import MDThemePicker


class Ustawienia(BoxLayout):
    """Klasa ustawień"""
    def open_language_selector(self):
        self.main_screen_manager.current = "language_settings"

    def open_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    def back_to_home_screen(self):
        self.nav_drawer.set_state('closed')
        self.main_screen_manager.current = "main_screen"

    def back_to_settings(self):
        self.main_screen_manager.current = "settings"

