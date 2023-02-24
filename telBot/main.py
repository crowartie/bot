import telebot
import json
import aiogram
from buttons import buttonsMainStructure, buttonsTest
from database import MySQLConnect, mainStructure, tests
from functions import funcTest

TOKEN = "5811670991:AAFedoSgHJapvryHLXwKdvXgyjdIPLV74h0"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message):
    if mainStructure.search_user(message.chat.id):

        bot.send_message(message.chat.id,
                         "С возвращением, мы рады снова вас видеть!!!",
                         reply_markup=buttonsMainStructure.start())
    else:
        bot.send_message(message.chat.id,
                         "Добро пожаловать на наш канал, я бот, обучающий математике.",
                         reply_markup=buttonsMainStructure.start())
        mainStructure.add_user(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "start")
def return_to_start(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.id, text="Вы вернулись в главное меню",
                          reply_markup=buttonsMainStructure.start())


@bot.callback_query_handler(func=lambda call: call.data == "tests")
def getTests(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.id, text="Тесты",
                          reply_markup=buttonsMainStructure.tests(mainStructure.get_tests()))


@bot.callback_query_handler(func=lambda call: call.data == "coursesForTraining")
def coursesForTraining(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          text="Курсы",
                          reply_markup=buttonsMainStructure.coursesForTraining(mainStructure.getCourses()))


@bot.callback_query_handler(func=lambda call: call.data == "re_showTests")
def re_showTests(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.id, text="Тесты",
                          reply_markup=buttonsMainStructure.tests(mainStructure.get_tests()))


@bot.callback_query_handler(func=lambda call: call.data.startswith("test"))
def test(call):
    if tests.search_test(call.data):
        if tests.search_test_action_user(call.message.chat.id, call.data):
            if tests.check_is_passed(call.message.chat.id, call.data):
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.id,
                                      text="Вы уже проходили данный тест, выберите другой",
                                      reply_markup=buttonsMainStructure.re_showTests())
                return
            elif tests.search_action_tests_user(call.message.chat.id):
                tests.clear_action_tests(call.message.chat.id)
        else:
            tests.create_action_user(call.message.chat.id, call.data)
        user = tests.get_action_user(call.message.chat.id, call.data)
        print(user)
        post = funcTest.get_question_in_message(user, call)
        if post is not None:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  text=post["question"],
                                  reply_markup=post["buttons"])
    else:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text="Тест ещё находится в разработке, просим прощения",
                              reply_markup=buttonsMainStructure.re_showTests())


@bot.callback_query_handler(func=lambda call: call.data.startswith("ans&"))
def answer(call):
    call.data = call.data[4:]
    print(call.data)
    actionTest = tests.search_action_test(call.message.chat.id)
    user = tests.get_action_user(call.message.chat.id, actionTest)
    if call.data == "1":
        user['result'] += 1
        tests.update_action_user(call.message.chat.id, {'result': user['result']})
    question = tests.get_question(user['callback'], user['numQuestion'])
    funcTest.show_answer(call, question)

    user['numQuestion'] += 1
    tests.update_action_user(call.message.chat.id,
                             {'numQuestion': user['numQuestion']})


@bot.callback_query_handler(func=lambda call: call.data == "nextQuestion")
def next(call):
    actionTest = tests.search_action_test(call.message.chat.id)
    user = tests.get_action_user(call.message.chat.id, actionTest)
    post = funcTest.get_question_in_message(user, call)
    if post is not None:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text=f"{user['numQuestion'] + 1}.{post['question']}", reply_markup=post["buttons"])


while True:
    bot.infinity_polling()
