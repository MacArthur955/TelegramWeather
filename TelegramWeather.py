import pprint
import sys, telebot
if __name__ != '__main__': sys.exit()
from DataBase import users, User
from Keys import Keys
from Languages import *
from datetime import datetime as d, timedelta


bot = Keys.makeBot()
map = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ', '🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿')


def keyboardInline(text, data, size, user):
    buttons = []
    for t,d in zip(text,data):
        if t[0] == '*' and (d == user.units or d in user.display): t = t.replace('*','✅   ')
        elif t[0] == '*': t = t.replace('*','')
        buttons.append(telebot.types.InlineKeyboardButton(t, callback_data=d))
    return telebot.types.InlineKeyboardMarkup(None, size).add(*buttons)
def readWeather(city,user,ID,message_id):
    weather = Keys.askWeather(**city, lang=user.lang, units=user.units)
    # pprint.pprint(weather)
    now = (d.fromtimestamp(weather['dt']) + timedelta(seconds=weather['timezone'])).strftime('%X')
    sunrise = (d.fromtimestamp(weather['sys']['sunrise']) + timedelta(seconds=weather['timezone'])).strftime('%X')
    sunset = (d.fromtimestamp(weather['sys']['sunset']) + timedelta(seconds=weather['timezone'])).strftime('%X')
    clouds = weather['clouds']['all']
    p = '🌞' if sunrise < now < sunset else '🌛'
    c = p if clouds < 10 else p+'☁' if clouds < 40 else '☁' if clouds < 70 else '☁☁'
    code = {'200': '🌧☁️🌩', '201': '🌧🌧🌩', '202': '🌧🌧⛈', '210': '🌩', '211': '☁️🌩', '212': '🌩☁️🌩', '221': '☁️☁️🌩', '230': '☁️🌩', '231': '🌧☁️🌩', '232': '☁☁⛈', '300': '☁️🌧', '301': '☁️☁️🌧', '302': '☁️🌧🌧', '310': '☁️☁️🌧', '311': '☁️🌧🌧', '312': '🌧🌧🌧', '313': '☁️☁️🌧', '314': '🌧🌧🌧', '321': '☁️🌧🌧', '500': c+'🌧', '501': c+'🌧', '502': '🌧🌧', '503': '🌧🌧🌧', '504': '🌧🌧🌧🌧', '511': '🌧🌨', '520': c+'🌧', '521': '🌧🌧', '522': '🌧🌧🌧', '531': '🌧☁️🌧', '600': c+'🌨', '601': c+'🌨🌨', '602': '🌨🌨🌨', '611': c+'🌧🌨', '612': c+'🌧🌨', '613': '🌧🌧🌨', '615': c+'🌧🌨', '616': '☁️🌧🌨', '620': c+'🌧🌨', '621': '☁️🌧🌨', '622': '🌧🌨🌧🌨', '701': '🌫🌫🌫', '711': '🌫🌫🌫', '721': '🌫🌫🌫', '731': '🌫🌫🌫', '741': '🌫🌫🌫', '751': '🌫🌫🌫', '761': '🌫🌫🌫', '762': '🌋🌫🌫', '771': '🌬💨💨', '781': '🌪', '800': p, '801': c, '802': c, '803': c, '804': c}
    symbol = {'metric':['℃','m/s'],'imperial':['℉','mph'],'standard':['K','m/s']}

    text = f"{code[str(weather['weather'][0]['id'])]}\n"
    if message_id: bot.edit_message_text(text,ID,message_id)
    else: bot.send_message(ID,text)
    text = f"{city['name']}     {city['country'].translate(map)}     {city['state'] if 'state' in city else ''}\n\n" \
           f"{weather['weather'][0]['description'].title()}\n\n"
    if 'temp' in user.display: text += f"{int(weather['main']['temp'])}  {symbol[user.units][0]}               🌡\n"
    if 'pressure' in user.display: text += f"{int(weather['main']['pressure'])}  hPa\n"
    if 'wind' in user.display: text += f"{int(weather['wind']['speed'])}  {symbol[user.units][1]}                  🎏\n"
    bot.send_message(ID,text)


@bot.message_handler(commands='start')
def receive_start(message):
    ID = message.chat.id
    if ID not in users: User(ID)
    user = users[ID]
    bot.send_message(ID, '🌏')
    bot.send_message(ID, START[user.lang], reply_markup=user.keyboard)
@bot.message_handler(commands='settings')
def receive_settings(message):
    ID = message.chat.id
    user = users[ID]
    bot.send_message(ID, '🔧')
    bot.send_message(ID, SETTINGS[user.lang][0], reply_markup=keyboardInline(SETTINGS[user.lang][1:],SETTINGS['data'],1,user))
@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    ID = call.message.chat.id
    user = users[ID]
    if call.data == 'lang': bot.edit_message_text(LANG[user.lang][0],ID,call.message.message_id,reply_markup=keyboardInline(LANG['buttons'],LANG['data'],1,user))
    elif call.data in LANG['data']:
        user.lang = call.data
        bot.answer_callback_query(call.id,LANG[user.lang][1])
        bot.edit_message_text(SETTINGS[user.lang][0],ID, call.message.message_id, reply_markup=keyboardInline(SETTINGS[user.lang][1:],SETTINGS['data'],1,user))
    elif call.data == 'unit': bot.edit_message_text(UNITS[user.lang]['message'],ID,call.message.message_id,reply_markup=keyboardInline(list(UNITS[user.lang].values())[1:-1],UNITS['data'],1,user))
    elif call.data in UNITS['data']:
        user.units = call.data
        bot.answer_callback_query(call.id,UNITS[user.lang]['answer'][user.units])
        bot.edit_message_text(SETTINGS[user.lang][0],ID, call.message.message_id, reply_markup=keyboardInline(SETTINGS[user.lang][1:],SETTINGS['data'],1,user))
    elif call.data == 'close': bot.delete_message(ID,call.message.message_id)
    elif call.data.isdecimal(): readWeather(user.cities[int(call.data)],user,ID,call.message.message_id)
@bot.message_handler(content_types='text')
def receive_text(message):
    ID = message.chat.id
    user = users[ID]
    user.cities = Keys.askCity(message.text,user.limit)
    if not user.cities: bot.send_message(ID,EMPTY[user.lang])
    elif len(user.cities) == 1: readWeather(user.cities[0],user,ID,'')
    else: bot.send_message(ID,CITIES[user.lang],reply_markup=keyboardInline(**{'text':[f"{city['name']}     {city['country'].translate(map)}     {city['state'] if 'state' in city else ''}" for city in user.cities],'data':[str(i) for i,city in enumerate(user.cities)]},size=1,user=user))


bot.polling()
