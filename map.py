from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty
import pandas as pd
from kivy.clock import Clock


class Map(MapView):
    """Klasa mapy"""

    get_marker_timer = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.countries_list = []
        self.loaded_markers = []
        self.menu_data = {
            'plus': 'Powiększ mape',
            'minus': 'Oddal mape',
            'information-variant': "Informacje",
            "map-marker-circle": 'Wyśrodkuj na mnie',
            'magnify': 'Znajdź',
        }

    def open_search_dialog(self):
        self.country_field.text = ""
        self.main_screen_manager.current = "search_dialog"

    def zoom_plus(self, *args):
        """Funckja przybliżająca mape"""
        self.zoom += 1

    def zoom_minus(self, *args):
        """Funckcja oddalająca mape mape"""
        self.zoom -= 1

    def center_on_me(self):
        """Funkcja środkująca mape na dancyh współrzędnych"""

    def menu_data_callback(self, instance):
        """Funkcja obsługująca menu"""

        if instance.icon == "minus":
            self.zoom_minus()
        elif instance.icon == "plus":
            self.zoom_plus()
        elif instance.icon == "map-marker-circle":
            self.center_on_me()
        elif instance.icon == "magnify":
            self.open_search_dialog()
        elif instance.icon == "information-variant":
            self.open_info()

    def load_csv_file(self):
        """Funkcja ładująca dane z pliku .csv"""

        col_list = ["country", "capital", "lat", "lon", "code", "continent"]

        self.data = pd.read_csv('countries.csv', error_bad_lines=False, encoding='cp1252', warn_bad_lines=False, sep=';'
                                , usecols=col_list, na_filter=False)

        self.countries_list = self.data.values.tolist()

    def start_get_markers_in_fov(self):
        """Funckja stopująca ładowanie się markerów przy ciągłym scrollowaniu"""
        try:
            self.get_marker_timer.cancel()

        except:
            pass

        self.get_marker_timer = Clock.schedule_once(self.get_markers_in_fov, 0.5)

    def get_markers_in_fov(self, *args):
        """Funckja ładująca markery"""

        # Sprawdzam współżędne każdego z rogów
        # Przypisuje je do pojedyńczych zmiennych
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()

        visible = self.data.loc[(self.data['lat'].between(min_lat, max_lat, inclusive=False))
                                & (self.data['lon'].between(min_lon, max_lon, inclusive=False))]

        visible_list = visible.values.tolist()

        # print(visible_list)

        self.add_markers_to_map(visible_list)

    def add_markers_to_map(self, visible_list):

        i = 0
        for country in visible_list:
            # print(visible_list[i])
            # print("Index:" + str(i) + "\n")

            lat = visible_list[i][2]
            lon = visible_list[i][3]
            country_name = visible_list[i][0]
            country_capital = visible_list[i][2]
            country_code = visible_list[i][4]

            marker = CovidMarker(lat=lat, lon=lon, country=country_name, capital=country_capital,
                                 code=country_code)

            if marker in self.loaded_markers:
                continue
            else:
                self.loaded_markers.append(marker)
                self.add_widget(marker)

            i += 1

    def go_to_country(self, latitude, lontitude):
        self.lat = latitude
        self.lon = lontitude
        self.zoom = 6

        print(self.lat, self.lon)


class CovidMarker(MapMarkerPopup):
    """Klasa markera na mapie"""
    def __init__(self, country, capital, code, **kwargs):
        super().__init__(**kwargs)

        self.source = "images/map_marker.png"

        self.country_name = country
        self.capital_name = capital
        self.country_code = code

    def on_release(self, *args):
        print(self.country_name)


class CustomOneLineIconListItem(OneLineIconListItem):
    """Klasa rzędu z listy krajów"""
    icon = StringProperty()


class SearchBox(Screen):
    def set_country_filter(self, text="", search=False):
        """Klasa filtrująca kraje"""

        self.rv.data = []

        for country_name in self.corona_map.countries_list:
            country = country_name[0]
            if search:
                if text in country:
                    self.rv.data.append({"viewclass": "CustomOneLineIconListItem",
                                         "icon": "earth",
                                         "text": country,
                                         })

            else:
                self.rv.data.append({"viewclass": "CustomOneLineIconListItem",
                                     "icon": "earth",
                                     "text": country,
                                     })

    def set_coordinates(self, country_name):
        """Funkcja ustawiająca koordynaty na wybrane państwo"""
        print(country_name)

        contry_list = self.corona_map.countries_list

        country_lat = None
        country_lon = None
        for country in contry_list:
            if country_name in country:
                print("Przenoszenie do:", country)
                country_lat = country[2]
                country_lon = country[3]

                self.corona_map.go_to_country(country_lat, country_lon)

                self.ustawienia.back_to_home_screen()

            else:
                pass




