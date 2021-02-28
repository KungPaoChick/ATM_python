import mysql.connector as connectSQL
import colorama


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def connect_db():
    mySQL = connectSQL.connect(
        host='localhost',
        user='root',
        password=''
    )
    myCursor = mySQL.cursor()

    run_once(check_database(myCursor))
    run_once(check_table(myCursor))
    myCursor.execute('USE ATM')
    return mySQL


@run_once
def check_database(cursor):
    try:
        cursor.execute(
            'CREATE DATABASE IF NOT EXISTS ATM')
        result = cursor.with_rows
        if result:
            cursor.execute('USE ATM')
            print(colorama.Fore.GREEN,
                '\n[*] Successfully Created Database: ATM', colorama.Style.RESET_ALL)
        else:
            cursor.execute('USE ATM')
    except connectSQL.Error as err:
        print(colorama.Fore.RED,
            '\n[!!] An Error has occured!', err, colorama.Style.RESET_ALL)


@run_once
def check_table(cursor):
    try:
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users(
                `Account_Number` VARCHAR(9) NOT NULL,
                `Card_Number` VARCHAR(16) NOT NULL,
                `CVV` INT(3) NOT NULL,
                `Name` VARCHAR(50) NOT NULL,
                `PIN` INT(6) NOT NULL,
                `Balance` INT(9),
                PRIMARY KEY (`Account_Number`));''')
        result = cursor.with_rows
        if result:
            print(colorama.Fore.GREEN,
                '\n[*] Successfully Created Table: users', colorama.Style.RESET_ALL)
        else:
            pass
    except connectSQL.Error as err:
        print(colorama.Fore.RED,
            '\n[!!] An Error has occured!', err, colorama.Style.RESET_ALL)


def insertData(connection, values, execution):
    val = [tuple(values)]
    cursor = connection.cursor()

    try:
        cursor.executemany(execution, val)
        cursor.execute('SELECT * FROM users')
        cursor.fetchall()
        connection.commit()
        print(colorama.Fore.YELLOW, cursor.rowcount,
            'was inserted', colorama.Style.RESET_ALL)
    except connectSQL.Error as err:
        print(colorama.Fore.RED,
            '[!!] An Error has occured!', err, colorama.Style.RESET_ALL)
