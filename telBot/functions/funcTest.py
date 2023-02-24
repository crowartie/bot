from database import MySQLConnect, mainStructure, tests
import telebot
import json
import aiogram
from buttons import buttonsMainStructure, buttonsTest
from database import MySQLConnect, mainStructure, tests
TOKEN = "5811670991:AAFedoSgHJapvryHLXwKdvXgyjdIPLV74h0"
bot = telebot.TeleBot(TOKEN)
def show_answer(call,question):
    text=""
    for i in tests.get_answer_option(question):
        if i['answer']=="0":
            text+=i['answerOption'] +" ❌\n"
        else:
            text += i['answerOption'] + " ✅\n"
    bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text=text,reply_markup=buttonsTest.next_question())

def get_question_in_message(user, call):
    print(user['numQuestion'])
    if int(user['numQuestion']) == int(user['max_result']):
        user['is_passed'] = 1
        user['is_passing'] = 0
        print(user['result'])
        user['numQuestion']=0
        tests.update_action_user(call.message.chat.id, {'is_passed': user['is_passed'], 'is_passing': user['is_passing'],
                                           'numQuestion': user['numQuestion'],
                                           'result': user['result']})

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text=f"Вы успешно прошли тест.\nВаш результат:{100/user['max_result']*user['result']:.1f}%",
                              reply_markup=buttonsMainStructure.return_to_home())
        return
    question = tests.get_question(user['callback'], user['numQuestion'])
    if question is None:
        return
    return {'question': question, "buttons": buttonsTest.getAnswers(tests.get_answer_option(question))}