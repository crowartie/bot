from telebot import types


class Commands:
    def start(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        buttons = [types.InlineKeyboardButton("Курсы для обучения", callback_data="coursesForTraining"),
                   types.InlineKeyboardButton("Тесты", callback_data="tests")]
        markup.add(buttons[0], buttons[1])
        return markup

    def coursesForTraining(self,listCourses):
        markup = types.InlineKeyboardMarkup()
        for course in listCourses:
            markup.add(types.InlineKeyboardButton(course['name'], callback_data='callback'))
        markup.add(types.InlineKeyboardButton("Вернуться в главное меню", callback_data='start'))
        return markup
    def tests(self,listTests):
        markup = types.InlineKeyboardMarkup()
        for test in listTests:
            markup.add(types.InlineKeyboardButton(test['name'], callback_data=test['callback']))
        markup.add(types.InlineKeyboardButton("Вернуться в главное меню", callback_data='start'))
        return markup
    def getAnswers(self,list):
        markup = types.InlineKeyboardMarkup()
        for i in list:
            print(i['answerOption'],i['answer'])
            markup.add(types.InlineKeyboardButton(i['answerOption'], callback_data="ans&"+i['answer']))
        return markup


