
# Moduły kivy
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from main import Zdrowie

# Reszta modułów
from functools import partial
from bs4 import BeautifulSoup
import pandas as pd


class Map(MapView):
    """Klasa mapy"""

    get_marker_timer = None
    website_content = []
    updated_data_list = []
    updated_data = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.result = None
        self.source = None
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
        """Funkcja otwierająca okienko szukania"""
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

    def get_cases_data(self):
        """Webscrapper który pobiera dane z internetu"""

        try:
            self.result = UrlRequest("https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data",
                                     on_success=partial(self.update_file),
                                     verify=False)
        except Exception as e:
            print(e)

    def update_file(self, *args):
        """Funkcja aktualizująca plik countries_pl.csv"""
        self.source = self.result.result

        # Czyszcze liste website_content żeby nie ładować danych drugi raz przy refreshu
        self.website_content.clear()

        soup = BeautifulSoup(self.source, 'lxml')

        covid_data_container = soup.find("table", attrs={"id": "thetable"})

        covid_data_container_body = soup.find("tbody")

        covid_data_rows = covid_data_container_body.findAll("tr")

        for country_row in covid_data_rows[1:]:
            small_flag_image_source = country_row.find("img")
            image_source = "No data"

            try:
                # Przypisuje adres zdjęcia flagi do zmiennej i podmieniam rozdzielczość
                small_flag_image_source = small_flag_image_source.attrs["src"]
                image_source = small_flag_image_source.replace("23px", "720px")
                image_source = image_source.replace("//", "https://")

            except AttributeError:
                small_flag_image_source = "No data"

            # Przypisuje nazwe kraju do zmiennej
            country_name = country_row.find("a").contents[0]

            # Przypisuje wartości domyślne
            cases = "No data"
            deaths = "No data"
            recoveries = "No data"
            cases_deaths_recov_container = []
            cases_deaths_recov_list = []

            try:
                cases_deaths_recov_container = country_row.findAll("td")

                # Loop znajdujący wszystkie rzędy informacji ze storny
                for column in cases_deaths_recov_container[:3]:
                    check = column.find("span")
                    if check is None:
                        cases_deaths_recov_list.append(column.contents[0])
                try:
                    try:
                        cases = cases_deaths_recov_list[0]
                        cases = cases.replace("\n", "")
                    except IndexError or KeyError:
                        pass

                    try:
                        deaths = cases_deaths_recov_list[1]
                        deaths = deaths.replace("\n", "")
                    except IndexError or KeyError:
                        pass

                    try:
                        recoveries = cases_deaths_recov_list[2]
                        recoveries = recoveries.replace("\n", "")

                    except IndexError or KeyError:
                        pass

                except IndexError:
                    pass

            except AttributeError:
                pass

            country_data = [country_name, cases, deaths, recoveries, image_source]

            self.website_content.append(country_data)

        # print(self.website_content)

        # Teraz pobrane dane dodaje do pliku .csv
        col_list = ["country", "capital", "lat", "lon", "code", "polish", "cases", "deaths", "recov", "flag_src"]

        df = pd.read_csv('countries_pl.csv', error_bad_lines=False, encoding='cp1252', warn_bad_lines=False,
                         sep=';', usecols=col_list, na_filter=False)

        data_list = df.values.tolist()

        self.updated_data_list = []

        # List nazw samych państw, która przyda się później
        only_country_names_list = []

        # Loop którym aktualizuje liste państw o liczbe zakażeń
        for data in data_list:
            for country in self.website_content:
                if data[0] == country[0]:
                    cases = country[1]
                    deaths = country[2]
                    recoveries = country[3]

                    value_cases = data[6]
                    value_deaths = data[7]
                    value_recoveries = data[8]

                    value_cases = cases
                    value_deaths = deaths
                    value_recoveries = recoveries

                    updated_country_info = [data[0], data[1], data[2], data[3], data[4], data[5],
                                            value_cases, value_deaths, value_recoveries, country[4]]

                    self.updated_data_list.append(updated_country_info)

                    only_country_names_list.append(country[0])

                else:
                    pass

        # Uzupełniam zaktualizowaną liste o państwa które nie miały inforacji o zakażeniach, aby
        # utrzymać spójność alfabetyczną
        for data in data_list:
            if data[0] in only_country_names_list:
                # print(data[0], "jest już na liście")
                pass
            else:
                # print("Dodano", data[0])
                self.updated_data_list.append(data)

        col_list = ["country", "capital", "lat", "lon", "code", "polish", "cases", "deaths", "recov", "flag_src"]

        self.updated_data = pd.DataFrame(self.updated_data_list, columns=col_list)

        self.countries_list = self.updated_data.values.tolist()

        self.search_box.set_country_filter()

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

        visible = self.updated_data.loc[(self.updated_data['lat'].between(min_lat, max_lat, inclusive=False))
                                & (self.updated_data['lon'].between(min_lon, max_lon, inclusive=False))]

        visible_list = visible.values.tolist()

        self.add_markers_to_map(visible_list)

    def add_markers_to_map(self, visible_list):

        i = 0
        for country in visible_list:

            lat = visible_list[i][2]
            lon = visible_list[i][3]
            country_name_en = visible_list[i][0]
            country_name_pl = visible_list[i][5]
            country_capital = visible_list[i][2]
            country_code = visible_list[i][4]
            country_cases = visible_list[i][6]
            country_deaths = visible_list[i][7]
            country_recoveries = visible_list[i][8]
            country_image = visible_list[i][9]

            marker = CovidMarker(lat=lat, lon=lon, country_en=country_name_en, country_pl=country_name_pl,
                                 capital=country_capital, code=country_code, cases=country_cases,
                                 deaths=country_deaths, recoveries=country_recoveries, image=country_image)

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
        self.zoom -= 1

        print(self.lat, self.lon)


class CovidMarker(MapMarkerPopup):
    """Klasa markera na mapie"""
    def __init__(self, country_pl, country_en, capital, code, cases, deaths, recoveries, image, **kwargs):
        super().__init__(**kwargs)
        self.app = Zdrowie()

        self.country_name_pl = country_pl
        self.country_name_en = country_en
        self.capital_name = capital
        self.country_code = code
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.image = image

        # W zależności od ilości zakżeń, przypisuje markerowi inny kolor
        self.cases_int = self.cases.replace(",", "")

        try:
            if 50000 > int(self.cases_int) > 0:
                self.source = "images/map_marker_low.png"
            elif 100000 > int(self.cases_int) >= 50000:
                self.source = "images/map_marker_more.png"
            elif 250000 > int(self.cases_int) >= 100000:
                self.source = "images/map_marker_medium.png"
            elif 400000 > int(self.cases_int) >= 250000:
                self.source = "images/map_marker.png"
            elif int(self.cases_int) >= 400000:
                self.source = "images/map_marker_extreme.png"
            else:
                self.source = "images/map_marker_no_data.png"

        except ValueError:
            # Jeżeli wyskakuje nam ValueError to oznacza, że dany plik nie ma danych
            self.source = "images/map_marker_no_data.png"

    def open_dialog(self):
        if self.parent.parent.language == "pl":
            title = "Informacje z kraju:"
        else:
            title = "Country data:"

        self.country_dialog = CountryDialog(title=title)

        self.country_dialog.cases = self.cases
        self.country_dialog.deaths = self.deaths
        self.country_dialog.recoveries = self.recoveries
        self.country_dialog.flag_source = self.image

        if self.parent.parent.language == "pl":
            self.country_dialog.country_name = self.country_name_pl
        else:
            self.country_dialog.country_name = self.country_name_en

        # print(self.country_dialog.flag_source)

        self.country_dialog.open()

    def on_release(self, *args):

        if self.app.language == "pl":
            print(self.country_name_pl, self.cases, self.deaths, self.recoveries)
        else:
            print(self.country_name_en, self.cases, self.deaths, self.recoveries)

        self.open_dialog()

    def remove_dialog(self):
        self.remove_widget(self.country_dialog)


class CustomOneLineIconListItem(OneLineIconListItem):
    """Klasa rzędu z listy krajów"""
    icon = StringProperty()


class SearchBox(Screen):
    app = Zdrowie()

    def set_country_filter(self, text="", search=False):
        """Klasa filtrująca kraje"""

        self.rv.data = []

        for country_name in self.corona_map.countries_list:

            if self.app.language == "pl":
                country = country_name[5]
            else:
                country = country_name[0]

            capital_text = text.capitalize()
            if search:
                if capital_text in country:
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
        # print(country_name)

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


class CountryDialog(Popup):
    """Klasa dialogu otwierającego się po kliknięciu markera"""
    cases = StringProperty()
    deaths = StringProperty()
    recoveries = StringProperty()
    country_name = StringProperty()
    flag_source = StringProperty()
