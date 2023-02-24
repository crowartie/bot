from main import bot


class ButtonHandler:
    def buttonsWithCommand(self,button):
        if button == "coursesForTraining":
            bot.send_message(call.message.chat.id, "11111")
        elif call.data == "tests":
            bot.send_message(call.message.chat.id, "2222")