import telebot

from commands import Commands

commands = Commands()
from dataBase import MySQL
from commands import Commands

TOKEN = "5811670991:AAFedoSgHJapvryHLXwKdvXgyjdIPLV74h0"
bot = telebot.TeleBot(TOKEN)
mysql = MySQL('localhost', 3306, 'root', '', 'telBot')


class Quiz:
    def __init__(self, actionTest,dataUser):
        self.questions = mysql.get_uestions(actionTest)
        self.user=dataUser
    def send_question(self, call, numQuestion):
        bot.send_message(self.user['chat_id'], self.questions[self.user['question_index']]['question'],
                         reply_markup=commands.getAnswers(
                         mysql.getTest(self.questions[numQuestion]['question'])))

    def check(self, call):
        print(call.data)
        if call.data == "1":
            bot.send_message(self.user['chat_id'], "Верно!!!")
        elif call.data == "0":
            bot.send_message(self.user['chat_id'],
                             f"Неверно. \nПравильный ответ: "
                             f"{mysql.get_true_answer(self.questions[self.user['question_index']]['question'])}")
        self.user['question_index']+=1
        self.user['is_passing'] -= 1
        self.user['is_passed']+=1
        print(self.user['question_index'])
        print(self.user)
