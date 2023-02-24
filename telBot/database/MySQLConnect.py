import pymysql



def connect(host, port, user, password, db_name):
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
    )
        return connection
