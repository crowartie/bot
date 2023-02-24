from database import MySQLConnect

connection = MySQLConnect.connect('localhost', 3306, 'root', '', 'telBot')


def search_test(test):
    select = f"""
             select COUNT(DISTINCT(questions.question)) AS count 
             FROM answers 
             JOIN tests ON answers.id_test=tests.id 
             JOIN questions ON answers.id_question=questions.id 
             WHERE tests.callback='{test}';"""
    with connection.cursor() as cursor:
        cursor.execute(select)
        countQuestions = cursor.fetchone()
        
    return countQuestions['count']


def search_test_action_user(chat_id, test):
    select = f"""
             SELECT count(*) as count 
             FROM statusUsers 
             JOIN users ON statusUsers.user_id=users.id 
             JOIN tests ON statusUsers.test_id=tests.id 
             WHERE users.users='{chat_id}' and tests.callback='{test}';
             """
    with connection.cursor() as cursor:
        cursor.execute(select)
        findUser = cursor.fetchone()
        print(findUser['count'])
    return findUser['count']


def check_is_passed(user_id, test):
    select = f"""
             SELECT count(*) as count From statusUsers
             JOIN users ON statusUsers.user_id=users.id
             JOIN tests ON statusUsers.test_id=tests.id
             WHERE users.users='{user_id}' and tests.callback='{test}' and is_passed=1
             """
    with connection.cursor() as cursor:
        cursor.execute(select)
        findUser = cursor.fetchone()
        
    return findUser['count']


def search_action_tests_user(user_id):
    select = f"""
             SELECT count(*) as count
             From statusUsers 
             JOIN users ON statusUsers.user_id=users.id
             WHERE users.users='{user_id}' AND is_passing = 1; 
             """
    with connection.cursor() as cursor:
        cursor.execute(select)
        findActionTests = cursor.fetchone()
        
    return findActionTests['count']


def clear_action_tests(user_id):
    select = f"""
             UPDATE statusUsers 
             SET  is_passing = 0 
             WHERE statusUsers.user_id=(SELECT id FROM users WHERE users='{user_id}')
             """
    with connection.cursor() as cursor:
        cursor.execute(select)
        connection.commit()
        

def create_action_user(user_id, test):
    select = f"""
             INSERT INTO `statusUsers`(`user_id`, `test_id`, `numQuestion`, 
                                       `is_passing`, `is_passed`, `result`, `max_result`)
             VALUES ((SELECT id FROM users WHERE users.users='{user_id}') , 
                     (SELECT id FROM tests WHERE tests.callback='{test}'), 
                     0, 1, 0, 0, (select COUNT(DISTINCT(questions.question)) AS countQuestions
                                  FROM answers 
                                  JOIN tests ON answers.id_test=tests.id 
                                  JOIN questions ON answers.id_question=questions.id 
                                  WHERE tests.callback='{test}'))
             """
    with connection.cursor() as cursor:
        cursor.execute(select)
        connection.commit()
        

def get_action_user( chat_id, test):
    select1 = f"""
             UPDATE statusUsers SET is_passing = 1 
             WHERE statusUsers.user_id=(SELECT id FROM users WHERE users='{chat_id}')
             AND statusUsers.test_id=(SELECT id FROM tests WHERE callback='{test}');
             """
    select2=f"""
             SELECT users.users,tests.callback,numQuestion,is_passing,is_passed,result, max_result 
             FROM statusUsers 
             JOIN users ON statusUsers.user_id=users.id 
             JOIN tests ON statusUsers.test_id=tests.id 
             WHERE users.users='{chat_id}' AND tests.callback = '{test}';
             """
    with connection.cursor() as cursor:
        cursor.execute(select1)
        connection.commit()
        cursor.execute(select2)
        user = cursor.fetchone()
        print(user)
        
    return user
def update_action_user(chat_id, data):
    with connection.cursor() as cursor:
        for item in data.items():
            print(item[0], item[1])
            select = f"""UPDATE statusUsers SET {item[0]} = '{item[1]}'
                     WHERE statusUsers.user_id=(SELECT id FROM users WHERE users='{chat_id}')"""
            cursor.execute(select)
            connection.commit()

def search_action_test(chat_id):
    select = f"""
             SELECT tests.callback AS test
             FROM statusUsers 
             JOIN users ON statusUsers.user_id=users.id 
             JOIN tests ON statusUsers.test_id=tests.id 
             WHERE users.users='{chat_id}' AND statusUsers.is_passing=1
            """
    with connection.cursor() as cursor:
        cursor.execute(select)
        q = cursor.fetchone()
    return q['test']

def get_question(actionTest, indexQuestion):
    select = f"""
                       SELECT DISTINCT(questions.question) AS question
                       FROM answers 
                       JOIN questions ON answers.id_question=questions.id 
                       JOIN tests ON answers.id_test=(SELECT id FROM tests WHERE tests.callback='{actionTest}')"""
    with connection.cursor() as cursor:
        cursor.execute(select)
        question = cursor.fetchall()
        return question[indexQuestion]['question']

def get_answer_option(question):

    select = f"""
             SELECT answers.answerOption AS answerOption, answers.answer AS answer
             FROM answers
             JOIN questions ON answers.id_question=questions.id
             JOIN tests ON answers.id_test=tests.id 
             WHERE questions.question='{question}'
            """
    with connection.cursor() as cursor:
        cursor.execute(select)
        answerOption = cursor.fetchall()
        print(answerOption)
    return answerOption
def get_true_answer(question):
    select = f"""
             SELECT answers.answerOption AS tryAnswer 
             FROM answers 
             JOIN tests ON answers.id_test=tests.id 
             JOIN questions ON answers.id_question=questions.id 
             WHERE questions.question='{question}' AND answers.answer='1'
             """
    with connection.cursor() as cursor:
        cursor.execute(select)
        trueAnswer = cursor.fetchone()
        return trueAnswer['tryAnswer']