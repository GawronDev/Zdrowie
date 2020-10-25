from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from phone_numbers import Show
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
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

    def calculate_covid_value(self):

        try:
            self.covid_cases_int = self.covid_cases.replace(",", "")
            self.covid_deaths_int = self.covid_deaths.replace(",", "")
            self.covid_recoveries_int = self.covid_recoveries.replace(",", "")

            total = int(self.covid_cases_int) + int(self.covid_deaths_int)
            self.covid_value = int(self.covid_cases_int) / total * 100

        except ValueError:
            pass

        self.covid_cases_value_text = "Zachorowania: " + self.covid_cases
        self.covid_recoveries_value_text = "Wyzdrowienia: " + self.covid_recoveries
        self.covid_deaths_value_text = "Śmierci: " + self.covid_deaths

        self.header_text = "COVID-19 w " + self.default_country[5] + ":"

    def update_default_country(self, new_country):
        self.default_country = new_country
        self.update_values()

    def update_article(self):
        list = self.aktualnosci.website_content

        print(list[4])

        self.article_image = list[4][0]
        self.article_header = list[4][1]
        self.article_text = list[4][2]
        self.article_link = list[4][3]

        self.image = self.article_image
        self.header = self.article_header
        self.sub_text = self.article_text
        self.link = self.article_link