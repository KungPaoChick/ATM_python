import db_connect


def get_all():
    mysql = db_connect.connect_db()
    cursor = mysql.cursor()
    cursor.execute('SELECT * FROM users')
    print([i[0] for i in cursor.description])
    for result in cursor.fetchall():
        print(result)

get_all()
