import datetime

import requests
import bs4



# 
class Parser:
    """docstring for Parser"""
    def __init__(self, city):
        self._base_url = 'https://sinoptik.ua/погода-%s'
        self._city = city

    # 
    def set_city(self, city):
        self._city = city

    # 
    def get_html(self):
        page = requests.get(self._base_url % self._city)
        html = bs4.BeautifulSoup(page.text, 'html.parser')       
        return html

    # 
    def parse_html(self, html):
        months = html.select('.main .month')
        days = html.select('.main .day-link')
        dates = html.select('.main .date')
        min_temps = html.select('.main .min')
        max_temps = html.select('.main .max')
        data = {}

        day = datetime.datetime.now().day
        for i in range(0, 7):
            data.update({day+i: {
                'day': days[i].getText(),
                'date': dates[i].getText(),
                'month': months[i].getText(),
                'max_temperature': max_temps[i].getText(),
                'min_temperature': min_temps[i].getText()}
            })

        return data

    # 
    def get_weather(self):
        try:
            html = self.get_html()
            data = self.parse_html(html)
        except Exception:
            return None
        else:
            return data