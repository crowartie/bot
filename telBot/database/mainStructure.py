from database import MySQLConnect

connection = MySQLConnect.connect('localhost', 3306, 'root', '', 'telBot')


def add_user(userId):
    select = f"insert into users(users) values ({userId})"
    with connection.cursor() as cursor:
        cursor.execute(select)
        connection.commit()
        


def search_user(userId):
    select = f"select users from users where users={userId}"
    with connection.cursor() as cursor:
        result=cursor.execute(select)
        
    return result


def get_tests():
    select = f"select name, callback from tests"
    with connection.cursor() as cursor:
        cursor.execute(select)
        result = cursor.fetchall()
    return result

def getCourses():
    select = f"select name, callback from courses"
    with connection.cursor() as cursor:
        cursor.execute(select)
        courses = cursor.fetchall()
        
    return courses
