from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from phone_numbers import Show
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.clock import Clock
from phone_numbers import Show


class CustomList(OneLineIconListItem):
    def __init__(self, **kwargs):
        super(CustomList, self).__init__(**kwargs)
        self.add_widget(IconLeftWidget(icon='phone'))


class HomePage(BoxLayout):
    covid_value = NumericProperty()
    covid_cases = StringProperty()
    covid_deaths = StringProperty()
    covid_recoveries = StringProperty()
    covid_cases_int = NumericProperty()
    covid_deaths_int = NumericProperty()
    covid_recoveries_int = NumericProperty()
    covid_cases_value_text = StringProperty()
    covid_deaths_value_text = StringProperty()
    covid_recoveries_value_text = StringProperty()

    article_image = StringProperty()
    article_header = StringProperty()
    article_text = StringProperty()
    article_link = StringProperty()

    image = "images/white_background.png"
    sub_text = StringProperty()
    header = StringProperty()
    link = StringProperty()

    header = ""
    link = ""
    sub_text = ""

    default_country = ListProperty()
    header_text = StringProperty()

    default_country = ['Poland', 'Warsaw', 52.25, 21.0, 'PL', 'Polska', '253,688', '4,438', '112,619',
                       'https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Flag_of_Poland.svg/720px-Flag_of_Poland.svg.png']

    def update_values(self):
        list = self.corona_map.updated_data_list

        for country in list:

            if country[0] == self.default_country[0]:
                print(country)
                self.covid_cases = country[6]
                self.covid_deaths = country[7]
                self.covid_recoveries = country[8]

                self.calculate_covid_value()

            else:
                pass

        self.add_phone_numbers()

    def calculate_covid_value(self):

        try:
            self.covid_cases_int = self.covid_cases.replace(",", "")
            self.covid_deaths_int = self.covid_deaths.replace(",", "")
            self.covid_recoveries_int = self.covid_recoveries.replace(",", "")

            total = int(self.covid_cases_int) + int(self.covid_recoveries_int)
            self.covid_value = int(self.covid_cases_int) / total * 100

        except ValueError:
            pass

        self.covid_cases_value_text = "Zachorowania: " + self.covid_cases
        self.covid_recoveries_value_text = "Wyzdrowienia: " + self.covid_recoveries
        self.covid_deaths_value_text = "Śmierci: " + self.covid_deaths

        country = self.default_country[5]

        try:
            country = self.default_country[5].replace("ê", "ę")

        except Exception:
            pass

        try:
            country = self.default_country[5].replace("³", "ł")

        except Exception:
            pass

        self.header_text = "COVID-19 w " + country + ":"

    def update_default_country(self, new_country):
        self.default_country = new_country

        self.reset_numbers()

        self.update_values()

    def reset_numbers(self):
        self.numbers_container.clear_widgets()

    def update_article(self):
        list = self.aktualnosci.website_content

        self.article_image = list[4][0]
        self.article_header = list[4][1]
        self.article_text = list[4][2]
        self.article_link = list[4][3]

    def refresh_callback(self):
        def callback(interval):
            self.update_values()
            self.update_article()
            self.root.ids.scroll_view_home.refresh_done()
            self.app.tick = 0
            print("Odświeżono aktualności")

        Clock.schedule_once(callback, 1)

    def add_phone_numbers(self):
        self.data_first = Show.pickle_list(self)[0]

        country = self.default_country[5]

        try:
           country = self.default_country[5].replace("ê", "ę")

        except Exception:
            pass

        try:
            country = self.default_country[5].replace("³", "ł")

        except Exception:
            pass

        self.data_second = Show.pickle_list(self)[3][country]


        for i in range(len(self.data_first)):
            self.exp = MDExpansionPanel(icon=f'images/emergency/{self.data_first[i]}.png',
                                        content=CustomList(text=self.data_second[i]),
                                        panel_cls=MDExpansionPanelOneLine(
                                            text=self.data_first[i]
                                        ))
            self.numbers_container.add_widget(self.exp)

