from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
import pandas as pd
from kivy.clock import Clock


class Map(MapView):
    """Klasa mapy"""

    get_marker_timer = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.loaded_markets = []

    def load_csv_file(self):
        col_list = ["country", "capital", "lat", "lon", "code", "continent"]

        self.data = pd.read_csv('countries.csv', error_bad_lines=False, encoding='cp1252', warn_bad_lines=False, sep=';'
                                , usecols=col_list, na_filter=False)

    def start_get_markers_in_fov(self):
        """Funckja stopująca ładowanie się markerów przy ciągłym scrollowaniu"""
        try:
            self.get_marker_timer.cancel()

        except:
            pass

        self.get_marker_timer = Clock.schedule_once(self.get_markers_in_fov, 1)

    def get_markers_in_fov(self, *args):
        """Funckja ładująca markery"""

        # Sprawdzam współżędne każdego z rogów
        print(self.get_bbox())

        # Przypisuje je do pojedyńczych zmiennych
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()


        visible = self.data.loc[(self.data['lat'].between(min_lat, max_lat, inclusive=False)) & (self.data['lon'].between(min_lon, max_lon, inclusive=False))]

        visible_list = visible.values.tolist()

        print(visible_list)

        self.add_markers_to_map(visible_list)

    def add_markers_to_map(self, visible_list):

        i = 0
        for country in visible_list:
            print(visible_list[i])
            print("Index:" + str(i) + "\n")

            lat = visible_list[i][2]
            lon = visible_list[i][3]
            country_name = visible_list[i][0]
            country_capital = visible_list[i][2]
            country_code = visible_list[i][4]

            marker = CovidMarker(lat=lat, lon=lon, country=country_name, capital=country_capital,
                                 code=country_code)

            if marker in self.loaded_markets:
                continue
            else:
                self.loaded_markets.append(marker)
                self.add_widget(marker)

            i += 1

class CovidMarker(MapMarkerPopup):
    def __init__(self, country, capital, code, **kwargs):
        super().__init__(**kwargs)

        self.source = "images/map_marker.png"

        self.country_name = country
        self.capital_name = capital
        self.country_code = code

    def on_release(self, *args):
        print(self.country_name)

