from telebot import types


def start():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton("Курсы для обучения", callback_data="coursesForTraining"),
               types.InlineKeyboardButton("Тесты", callback_data="tests")]
    markup.add(buttons[0], buttons[1])
    return markup


def coursesForTraining(listCourses):
    markup = types.InlineKeyboardMarkup()
    for course in listCourses:
        markup.add(types.InlineKeyboardButton(course['name'], callback_data='callback'))
    markup.add(types.InlineKeyboardButton("Вернуться в главное меню", callback_data='start'))
    return markup


def tests(listTests):
    markup = types.InlineKeyboardMarkup()
    for test in listTests:
        markup.add(types.InlineKeyboardButton(test['name'], callback_data=test['callback']))
    markup.add(types.InlineKeyboardButton("Вернуться в главное меню", callback_data='start'))
    return markup

def re_showTests():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Показать тесты", callback_data='re_showTests'))
    return markup

def return_to_home():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Вернуться в гланое меню", callback_data='start'))
    return markup

