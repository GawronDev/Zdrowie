from kivy.uix.gridlayout import GridLayout


class Ustawienia(GridLayout):
    def back_to_home_screen(self):
        self.nav_drawer.set_state('closed')
        self.main_screen_manager.current = "main_screen"

    def back_to_settings(self):
        self.main_screen_manager.current = "settings"

