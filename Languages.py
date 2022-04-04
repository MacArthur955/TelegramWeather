import sys
if __name__ == '__main__': sys.exit()

START = {
    'en':'Type to me a name of a city, and i will tell you what\'s the weather there 😊',
    'pl':'Napisz do mnie nazwę miasta, a powiem ci jaka jest tam pogoda 😊'
}
SETTINGS = {
    'data':['lang','unit','display','close'],
    'en':['Choose a setting','Choose language   🇬🇧','Change units     🔡','Displayed conditions     🌤❄️🌈','Close      ❌'],
    'pl': ['Wybierz opcję','Wybierz język   🇵🇱', 'Zmień jednostki     🔡','Wyświetlane warunki     🌤❄️🌈' ,'Zamknij       ❌']
}
LANG = {
    'data': ['en','pl'],
    'buttons': ['English 🇬🇧', 'Polski 🇵🇱'],
    'en':['Choose language','You choosed English'],
    'pl':['Wybierz język','Wybrałeś język Polski']
}
UNITS = {
    'data': ['metric','imperial','standard'],
    'en': {'message':'What is more familiar to you? 🤔',
           'metric':'*25 °Celsius     8 kilometers per second',
           'imperial':'*77 °Fahrenheit     5 Miles per hour',
           'standard':'*298 Kelvin     8 kilometers per second',
           'answer': {'metric': 'You chose the metric system',
                      'imperial': 'You chose the imperial system',
                      'standard': 'You chose the standard system'}
           },
    'pl': {'message':'Co jest ci bardziej znane? 🤔',
           'metric': '*25 °celsjusza     8 kilometrów na sekunde',
           'imperial': '*77 °fahrenheita     5 mili na godzine',
           'standard': '*298 Kelwinów     8 kilometrów na sekunde',
           'answer': {'metric': 'Wybrałeś system metryczny',
                      'imperial': 'Wybrałeś system imperialny',
                      'standard': 'Wybrałeś system standardowy'}
           }
}
EMPTY = {
    'en':'I couldn\'t find such a city 🤔',
    'pl':'Nie mogłem znaleźć takiego miasta 🤔'
}
CITIES = {
    'en':'Where are we going this time?  😁',
    'pl':'Gdzie teraz idziemy? 😁'
}