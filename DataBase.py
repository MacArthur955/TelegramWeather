import sys, atexit, telebot, pickle
if __name__ == '__main__': sys.exit()

class User():
    def __init__(self,chatID):
        self.__lang = 'en'
        self.__units = 'metric' # standard, imperial
        self.limit = 3
        self.cities = list()
        self.display = ['temp','pressure','wind']
        users[chatID] = self
        self.saveData()
    @property
    def keyboard(self):
            return telebot.types.ReplyKeyboardMarkup(True, False, True).add(*self.cities+['/settings'])
    @property
    def lang(self):
        return self.__lang
    @lang.setter
    def lang(self,value):
        self.__lang = value
        self.saveData()
    @property
    def units(self):
        return self.__units
    @units.setter
    def units(self, value):
        self.__units = value
        self.saveData()
    def saveData(self):
        with open('users.pkl','wb') as file:
            pickle.dump(users,file)

try: file = open('users.pkl','rb')
except:
    file = open('users.pkl','x')
    users = dict()
else:
    users = pickle.load(file)
    print(users)
finally: file.close()
