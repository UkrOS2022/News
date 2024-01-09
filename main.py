from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import requests

API_KEY = 'c0d549ee75209d8ee82a821d1fd77d5b'
CITY_NAME = ''

NEWS_API_KEY = '3fe163b9e2d44cb08ed2dc48578f1c52'
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/top-headlines'
NEWS_API_PARAMS = {'country': 'ua', 'apiKey': NEWS_API_KEY}

class News(QWidget):
    def __init__(self):
        super().__init__()

        # STYLES

        buttons = """
            QPushButton {
                background-color: #B1B1B1;
                color: black;
                border: 2px solid #B1B1B1;
                border-radius: 5px;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #8B8B8B;
                color: white;
            }
        """
        
        h1 = """
            QLabel {
                font-size: 30px;
            }
        """

        self.saved_list = []

        # MAIN
        self.setWindowTitle(self.tr("News"))
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 400)
        icon = QIcon('icon.png')
        self.setWindowIcon(icon)
        self.setStyleSheet(buttons)

        # "WEATHER" LABEL
        self.weather_label = QLabel('Weather:', self)
        self.weather_label.setGeometry(5, 5, 210, 25)

        # "COMMUNITY" INPUT
        self.community_input = QLineEdit('Your community', self)
        self.community_input.setGeometry(5, 30, 210, 25)

        # "FIND" BUTTON
        self.find_button = QPushButton('Find', self)
        self.find_button.setGeometry(5, 60, 210, 35)
        self.find_button.clicked.connect(self.find)

        # "SAVED" LISTBOX
        self.saved_listbox = QListWidget(self)
        self.saved_listbox.setGeometry(5, 100, 210, 50)
        self.saved_listbox.itemClicked.connect(self.item_clicked)

        # "ADD" BUTTON
        self.add_button = QPushButton('Add', self)
        self.add_button.setGeometry(5, 155, 100, 35)
        self.add_button.clicked.connect(self.add)

        # "REMOVE" BUTTON
        self.remove_button = QPushButton('Remove', self)
        self.remove_button.setGeometry(110, 155, 105, 35)
        self.remove_button.clicked.connect(self.remove)

        # "CURRENCY" LABEL
        self.currency_label = QLabel('Currency:', self)
        self.currency_label.setGeometry(5, 195, 210, 25)

        # "MONEY" INPUT
        self.money_input = QLineEdit('Your money', self)
        self.money_input.setGeometry(5, 225, 155, 25)

        # "YOUR CURRENCY" COMBOBOX
        self.your_currency_combobox = QComboBox(self)
        self.your_currency_combobox.setGeometry(160, 225, 55, 25)
        self.your_currency_combobox.addItems(['USD', 'UAH', 'EUR'])

        # "CURRENCY" LABEL
        self.result_label = QLabel('Result: ', self)
        self.result_label.setGeometry(5, 250, 210, 25)

        # "TRANSLATE CURRENCY" COMBOBOX
        self.translate_currency_combobox = QComboBox(self)
        self.translate_currency_combobox.setGeometry(160, 250, 55, 25)
        self.translate_currency_combobox.addItems(['USD', 'UAH', 'EUR'])

        # "TRANSLATE" BUTTON
        self.translate_button = QPushButton('Translate', self)
        self.translate_button.setGeometry(5, 280, 210, 35)
        self.translate_button.clicked.connect(self.translate)

        # "ABOUT" BUTTON
        self.about_button = QPushButton('About', self)
        self.about_button.setGeometry(5, 330, 210, 35)
        self.about_button.clicked.connect(self.about)

        # "ABOUT" LABEL
        
        about = """
            News
            Version: 1.0.0
            Company: UkrOS
        """

        self.about_label = QLabel(about, self)
        self.about_label.setGeometry(250, 30, 190, 100)
        self.about_label.hide()

        # "NEWS" LABEL
        self.news_label = QLabel('', self)
        self.news_label.setGeometry(220, 5, 370, 390)

        # "WEATHER TODAY" LABEL
        self.weather_today_label = QLabel('Weather today: ', self)
        self.weather_today_label.setGeometry(250, 30, 190, 100)
        self.weather_today_label.hide()

        # "WEATHER TOMORROW" LABEL
        self.weather_tomorrow_label = QLabel('Weather tomorrow: ', self)
        self.weather_tomorrow_label.setGeometry(250, 135, 190, 100)
        self.weather_tomorrow_label.hide()

        # "GO TO NEWS" BUTTON
        self.go_to_button = QPushButton('Go to news', self)
        self.go_to_button.clicked.connect(self.go_to)
        self.go_to_button.setGeometry(250, 300, 210, 35)
        self.go_to_button.hide()

        self.load_saved_list()
        self.load_news()
        self.resizeEvent = self.on_resize


    # "LOAD NEWS" FUNCTION

    def load_news(self):
        response = requests.get(NEWS_API_ENDPOINT, params=NEWS_API_PARAMS)

        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])

            if articles:
                news_text = "\n".join([f"- {article['title']}" for article in articles])
                self.news_label.setText(news_text)
            else:
                self.news_label.setText('No news articles available')
        else:
            self.news_label.setText('Failed to fetch news. Please try again later')

    
    # "FIND" FUNCTION

    def find(self):
        # HIDE
        self.about_label.hide()
        self.news_label.hide()

        # SHOW
        self.weather_today_label.show()
        self.weather_tomorrow_label.show()
        self.go_to_button.show()
        
        CITY_NAME = self.community_input.text()
        url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Today's weather
            today_weather = data['weather'][0]['description']
            today_clouds = data['clouds']['all']
            today_pressure = data['main']['pressure']
            today_visibility = data['visibility']
            today_temp_min = data['main']['temp_min']
            today_temp_max = data['main']['temp_max']

            self.weather_today_label.setText(
                'In community ' + CITY_NAME + ':\nToday: ' + str(today_weather) + '\nClouds: ' + str(today_clouds) + '%'
                '\nPressure: ' + str(today_pressure) + ' mm\nVisibility: ' + str(int(today_visibility) // 1000) + ' km'
                '\nTemperature: Minumum ' + str(today_temp_min) + '°C\nTemperature: Maximum ' + str(today_temp_max) + '°C'
            )

            # Tomorrow's weather
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={CITY_NAME}&appid={API_KEY}&units=metric'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                tomorrow_weather = data['list'][8]['weather'][0]['description']
                tomorrow_clouds = data['list'][8]['clouds']['all']
                tomorrow_pressure = data['list'][8]['main']['pressure']
                tomorrow_visibility = data['list'][8]['visibility']
                tomorrow_temp_min = data['list'][8]['main']['temp_min']
                tomorrow_temp_max = data['list'][8]['main']['temp_max']

                self.weather_tomorrow_label.setText(
                'Tomorrow: ' + str(tomorrow_weather) + '\nClouds: ' + str(tomorrow_clouds) + '%'
                '\nPressure: ' + str(tomorrow_pressure) + ' mm\nVisibility: ' + str(int(tomorrow_visibility) // 1000) + ' km'
                '\nTemperature: Minumum ' + str(tomorrow_temp_min) + '°C\nTemperature: Maximum ' + str(tomorrow_temp_max) + '°C'
                )

    
    # LOAD SAVED LIST

    def load_saved_list(self):
        try:
            with open('file.txt', 'r') as f:
                self.saved_list = [line.strip() for line in f.readlines()]
                self.saved_listbox.addItems(self.saved_list)
        except FileNotFoundError:
            pass


    # CLOSING OF PROGRAMM
    
    def closeEvent(self, event):
        with open('file.txt', 'w') as f:
            for item in self.saved_list:
                f.write(f'{item}\n')
        event.accept()


    # "ITEM CLICKED" FUNCTION

    def item_clicked(self, item):
            selected_text = item.text()
            self.community_input.setText(selected_text)
            self.find()

    
    # "ADD" FUNCTION

    def add(self):
        text = self.community_input.text()
        self.saved_list.append(str(text))
        self.saved_listbox.clear()
        self.saved_listbox.addItems(self.saved_list)
    

    # "REMOVE" FUNCTION

    def remove(self):
        selected_item = self.saved_listbox.currentItem()
        if selected_item:
            text = selected_item.text()
            self.saved_list.remove(text)
            self.saved_listbox.clear()
            self.saved_listbox.addItems(self.saved_list)
    

    # "TRANSLATE" FUNCTION

    def translate(self):
        your_currency = self.your_currency_combobox.currentText().lower()
        translate_currency = self.translate_currency_combobox.currentText().lower()
        amount = float(self.money_input.text())

        url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{your_currency}/{translate_currency}.json'
        response = requests.get(url)

        if response.ok:
            exchange_rate = response.json()[translate_currency]
            result = amount * exchange_rate
            self.result_label.setText(f'Результат: {round(result, 2)} {translate_currency}')
        else:
            self.result_label.setText('Результат: 0')
    

    # "ABOUT" FUNCTION

    def about(self):
        # HIDE
        self.weather_today_label.hide()
        self.weather_tomorrow_label.hide()
        self.news_label.hide()

        # SHOW
        self.go_to_button.show()
        self.about_label.show()
    

    # "GO TO NEWS" FUNCTION

    def go_to(self):
        # HIDE
        self.weather_today_label.hide()
        self.weather_tomorrow_label.hide()
        self.go_to_button.hide()
        self.about_label.hide()

        # SHOW
        self.news_label.show()

        self.load_news()

    # Function to handle resizing event
    def on_resize(self, event):
        # Adjust the size of the news_label when the main window is resized
        new_size = event.size()
        self.news_label.setGeometry(220, 5, new_size.width() - 230, new_size.height() - 10)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = News()
    welcome_window.show()
    sys.exit(app.exec_())