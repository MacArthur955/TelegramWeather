import pprint
import sys, telebot
if __name__ != '__main__': sys.exit()
from DataBase import users, User
from Keys import Keys
from Languages import *
from datetime import datetime as d, timedelta


bot = Keys.makeBot()
map = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ', '๐ฆ๐ง๐จ๐ฉ๐ช๐ซ๐ฌ๐ญ๐ฎ๐ฏ๐ฐ๐ฑ๐ฒ๐ณ๐ด๐ต๐ถ๐ท๐ธ๐น๐บ๐ป๐ผ๐ฝ๐พ๐ฟ')


def keyboardInline(text, data, size, user):
    buttons = []
    for t,d in zip(text,data):
        if t[0] == '*' and (d == user.units or d in user.display): t = t.replace('*','โ   ')
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
    p = '๐' if sunrise < now < sunset else '๐'
    c = p if clouds < 10 else p+'โ' if clouds < 40 else 'โ' if clouds < 70 else 'โโ'
    code = {'200': '๐งโ๏ธ๐ฉ', '201': '๐ง๐ง๐ฉ', '202': '๐ง๐งโ', '210': '๐ฉ', '211': 'โ๏ธ๐ฉ', '212': '๐ฉโ๏ธ๐ฉ', '221': 'โ๏ธโ๏ธ๐ฉ', '230': 'โ๏ธ๐ฉ', '231': '๐งโ๏ธ๐ฉ', '232': 'โโโ', '300': 'โ๏ธ๐ง', '301': 'โ๏ธโ๏ธ๐ง', '302': 'โ๏ธ๐ง๐ง', '310': 'โ๏ธโ๏ธ๐ง', '311': 'โ๏ธ๐ง๐ง', '312': '๐ง๐ง๐ง', '313': 'โ๏ธโ๏ธ๐ง', '314': '๐ง๐ง๐ง', '321': 'โ๏ธ๐ง๐ง', '500': c+'๐ง', '501': c+'๐ง', '502': '๐ง๐ง', '503': '๐ง๐ง๐ง', '504': '๐ง๐ง๐ง๐ง', '511': '๐ง๐จ', '520': c+'๐ง', '521': '๐ง๐ง', '522': '๐ง๐ง๐ง', '531': '๐งโ๏ธ๐ง', '600': c+'๐จ', '601': c+'๐จ๐จ', '602': '๐จ๐จ๐จ', '611': c+'๐ง๐จ', '612': c+'๐ง๐จ', '613': '๐ง๐ง๐จ', '615': c+'๐ง๐จ', '616': 'โ๏ธ๐ง๐จ', '620': c+'๐ง๐จ', '621': 'โ๏ธ๐ง๐จ', '622': '๐ง๐จ๐ง๐จ', '701': '๐ซ๐ซ๐ซ', '711': '๐ซ๐ซ๐ซ', '721': '๐ซ๐ซ๐ซ', '731': '๐ซ๐ซ๐ซ', '741': '๐ซ๐ซ๐ซ', '751': '๐ซ๐ซ๐ซ', '761': '๐ซ๐ซ๐ซ', '762': '๐๐ซ๐ซ', '771': '๐ฌ๐จ๐จ', '781': '๐ช', '800': p, '801': c, '802': c, '803': c, '804': c}
    symbol = {'metric':['โ','m/s'],'imperial':['โ','mph'],'standard':['K','m/s']}

    text = f"{code[str(weather['weather'][0]['id'])]}\n"
    if message_id: bot.edit_message_text(text,ID,message_id)
    else: bot.send_message(ID,text)
    text = f"{city['name']}     {city['country'].translate(map)}     {city['state'] if 'state' in city else ''}\n\n" \
           f"{weather['weather'][0]['description'].title()}\n\n"
    if 'temp' in user.display: text += f"{int(weather['main']['temp'])}  {symbol[user.units][0]}               ๐ก\n"
    if 'pressure' in user.display: text += f"{int(weather['main']['pressure'])}  hPa\n"
    if 'wind' in user.display: text += f"{int(weather['wind']['speed'])}  {symbol[user.units][1]}                  ๐\n"
    bot.send_message(ID,text)


@bot.message_handler(commands='start')
def receive_start(message):
    ID = message.chat.id
    if ID not in users: User(ID)
    user = users[ID]
    bot.send_message(ID, '๐')
    bot.send_message(ID, START[user.lang], reply_markup=user.keyboard)
@bot.message_handler(commands='settings')
def receive_settings(message):
    ID = message.chat.id
    user = users[ID]
    bot.send_message(ID, '๐ง')
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
