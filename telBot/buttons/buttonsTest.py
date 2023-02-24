from telebot import types
def getAnswers(list):
    markup = types.InlineKeyboardMarkup()
    for i in list:
        print(i['answerOption'], i['answer'])
        markup.add(types.InlineKeyboardButton(i['answerOption'], callback_data="ans&" + i['answer']))
    markup.add(types.InlineKeyboardButton("Вернуться в главное меню", callback_data="start"))
    return markup
def next_question():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Следующий вопрос", callback_data="nextQuestion"))
    markup.add(types.InlineKeyboardButton("Вернуться в главное меню", callback_data="start"))
    return markup
