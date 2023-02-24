import pymysql


class MySQL:
    def __init__(self, host, port, user, password, db_name):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def add_user(self, userId):
        cursor = self.connection.cursor()
        select = f"insert into users(users) values ({userId})"
        cursor.execute(select)
        self.connection.commit()

    def search_user(self, userId):
        cursor = self.connection.cursor()
        select = f"select users from users where users={userId}"
        return cursor.execute(select)

    def get_tests(self):
        cursor = self.connection.cursor()
        select = f"select name, callback from tests"
        cursor.execute(select)
        return cursor.fetchall()

    def search_test(self, test):
        cursor = self.connection.cursor()
        select = f"select COUNT(DISTINCT(questions.question)) AS count " \
                 f"FROM answers " \
                 f"JOIN tests ON answers.id_test=tests.id " \
                 f"JOIN questions ON answers.id_question=questions.id " \
                 f"WHERE tests.callback='{test}';"
        cursor.execute(select)
        countQuestions = cursor.fetchall()
        if countQuestions:
            return countQuestions[0]['count']

        else:
            return 0

    def search_action_user(self, chat_id, test):
        cursor = self.connection.cursor()
        select = f"SELECT count(*) as count From statusUsers " \
                 f"JOIN users ON statusUsers.user_id=users.id " \
                 f"JOIN tests ON statusUsers.test_id=tests.id " \
                 f"WHERE users.users='{chat_id}' and tests.callback='{test}' "
        cursor.execute(select)
        findUser = cursor.fetchall()
        print(cursor.execute(select))
        if findUser:
            return findUser[0]['count']
        else:
            return 0

    def create_action_user(self, chat_id, test):
        cursor = self.connection.cursor()
        select = f"INSERT INTO `statusUsers`(`user_id`, `test_id`, `numQuestion`, " \
                 f"`is_passing`, `is_passed`, `result`, `max_result`) " \
                 f"VALUES ((SELECT id FROM users WHERE users.users='{chat_id}') , " \
                 f"(SELECT id FROM tests WHERE tests.callback='{test}'), 0, 1, 0, 0, " \
                 f"(select COUNT(DISTINCT(questions.question)) AS countQuestions " \
                 f"FROM answers " \
                 f"JOIN tests ON answers.id_test=tests.id " \
                 f"JOIN questions ON answers.id_question=questions.id " \
                 f"WHERE tests.callback='{test}'))"
        cursor.execute(select)
        self.connection.commit()

    def search_action_tests(self, chat_id):
        cursor = self.connection.cursor()
        select = f"SELECT count(*) as count " \
                 f"From statusUsers " \
                 f"JOIN users ON statusUsers.user_id=users.id " \
                 f"WHERE users.users='{chat_id}' AND statusUsers.is_passing = 1 "
        cursor.execute(select)

        countActionTests = cursor.fetchall()
        if countActionTests:

            return countActionTests[0]['count']
        else:
            return 0

    def clear_action_tests(self, chat_id):
        cursor = self.connection.cursor()
        select = f"UPDATE statusUsers SET numQuestion = 0, is_passing = 0, result = 0 " \
                 f"WHERE statusUsers.user_id=(SELECT id FROM users WHERE users='{chat_id}')"
        cursor.execute(select)
        self.connection.commit()

    def get_action_user(self, chat_id, test):
        cursor = self.connection.cursor()
        select = f"UPDATE statusUsers SET is_passing = 1 " \
                 f"WHERE statusUsers.user_id=(SELECT id FROM users WHERE users='{chat_id}') " \
                 f"AND statusUsers.test_id=(SELECT id FROM tests WHERE callback='{test}')"
        cursor.execute(select)
        self.connection.commit()
        select = f"SELECT users.users,tests.callback,numQuestion,is_passing,is_passed,result, max_result " \
                 f"FROM statusUsers " \
                 f"JOIN users ON statusUsers.user_id=users.id " \
                 f"JOIN tests ON statusUsers.test_id=tests.id " \
                 f"WHERE users.users='{chat_id}' AND tests.callback = '{test}'"
        cursor.execute(select)
        user = cursor.fetchall()
        return user

    def update_action_user(self, chat_id, data):
        cursor = self.connection.cursor()
        for item in data.items():
            print(item[0], item[1])
            select = f"UPDATE statusUsers SET {item[0]} = '{item[1]}' " \
                     f"WHERE statusUsers.user_id=(SELECT id FROM users WHERE users='{chat_id}')"
            cursor.execute(select)
            self.connection.commit()

    def searchActionTest(self, chat_id):
        cursor = self.connection.cursor()
        select = f"SELECT tests.callback AS test " \
                 f"FROM statusUsers " \
                 f"JOIN users ON statusUsers.user_id=users.id " \
                 f"JOIN tests ON statusUsers.test_id=tests.id " \
                 f"WHERE users.users='{chat_id}' AND statusUsers.is_passing=1"
        cursor.execute(select)
        q = cursor.fetchall()
        return q[0]['test']

    def get_question(self, actionTest, indexQuestion):
        cursor = self.connection.cursor()
        select_questions = f"SELECT DISTINCT(questions.question) AS question " \
                           f"FROM answers " \
                           f"JOIN questions ON answers.id_question=questions.id " \
                           f"JOIN tests ON answers.id_test=(SELECT id FROM tests WHERE tests.callback='{actionTest}')"
        cursor.execute(select_questions)
        question = cursor.fetchall()
        return question[indexQuestion]['question']

    def get_answer_option(self, question):
        cursor = self.connection.cursor()
        select = f"SELECT answers.answerOption AS answerOption, answers.answer AS answer " \
                 f"FROM answers " \
                 f"JOIN questions ON answers.id_question=questions.id " \
                 f"JOIN tests ON answers.id_test=tests.id " \
                 f"WHERE questions.question='{question}'"
        cursor.execute(select)
        answerOption = cursor.fetchall()
        return answerOption

    def get_true_answer(self, question):
        cursor = self.connection.cursor()
        select = f"SELECT answers.answerOption AS tryAnswer " \
                 f"FROM answers " \
                 f"JOIN tests ON answers.id_test=tests.id " \
                 f"JOIN questions ON answers.id_question=questions.id " \
                 f"WHERE questions.question='{question}' AND answers.answer='1'"
        cursor.execute(select)
        trueAnswer = cursor.fetchall()
        return trueAnswer[0]['tryAnswer']

    def getCourses(self):
        cursor = self.connection.cursor()
        select = f"select name, callback from courses"
        cursor.execute(select)
        courses = cursor.fetchall()
        return courses
