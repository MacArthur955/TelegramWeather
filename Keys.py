import pprint
import sys, telebot, requests
if __name__ == '__main__': sys.exit()

class Keys():
    __apiWeatherKey = 'Paste your api key here'
    __apiTelegramKey = 'Paste your api key here'
    @staticmethod
    def makeBot(): return telebot.TeleBot(Keys.__apiTelegramKey)
    @staticmethod
    def askCity(city,limit):
        return requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={Keys.__apiWeatherKey}').json()
    @staticmethod
    def askWeather(lat,lon,lang,units,**kwargs):
        return requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={Keys.__apiWeatherKey}&lang={lang}&units={units}').json()


