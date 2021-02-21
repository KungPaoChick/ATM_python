import mysql.connector as connectSQL
import colorama


def connect_db():
    mySQL = connectSQL.connect(
        host='127.0.0.1',
        user='root',
        passsword=''
    )
    return mySQL


def insertData(connection, values):
    myCursor = connection.cursor()
    sql = '''INSERT INTO
            users (Card_Number, Name, Address, Country, CVV, EXP)
            VALUES (%s,%s,%s,%s,%s,%s)'''

    val = [tuple(values)]
    try:
        myCursor.executemany(sql, val)
        myCursor.execute('SELECT * FROM users')
        myCursor.fetchall()
        connection.commit()
        print(colorama.Fore.YELLOW, myCursor.rowcount,
            'was inserted', colorama.Style.RESET_ALL)
    except connectSQL.Error as err:
        print(colorama.Fore.RED,
            '[!!] An Error has occured!', err, colorama.Style.RESET_ALL)