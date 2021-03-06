import db_connect
import colorama
import getpass
import fast_luhn as fl
import actions
from base64 import b64decode
import hashlib


class ATM:

    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin


    def login(self):
        cursor.execute(f'SELECT Name FROM users WHERE Card_Number={self.card_number}')

        for result in cursor.fetchone():
            print(colorama.Fore.GREEN,
                f'[*] Welcome, {result}!', colorama.Style.RESET_ALL)
            options(self.card_number, self.pin)


def options(card, pin):
    options = {
        1 : '1. Check Balance',
        2 : '2. Withdraw',
        3 : '3. Deposit',
        4 : '4. Exit'
    }

    while True:
        print('\n\n\n')
        for option in options:
            print(options[option])

        selection = int(input('Enter digit to choose: '))
        data = []

        if selection in options:
            print('\n\n\n')
            data.extend((selection, cursor, mysql, card, pin))
            if selection == 4:
                cursor.execute(f'SELECT Name FROM users WHERE Card_Number={card}')
                for result in cursor.fetchone():
                    print(colorama.Fore.GREEN,
                    f'\n[*] Goodbye, {result}. And Thank you!\n', colorama.Style.RESET_ALL)
                    quit()
            actions.action(data)
        else:
            print(colorama.Fore.RED,
                '[!!] Something went wrong', colorama.Style.RESET_ALL)


def verify(pin):
    cursor.execute(f'SELECT PIN FROM users WHERE Card_Number={card}')
    for x in cursor.fetchone():
        salt_from_pin = x[:88]
        key_from_pin = x[88:]

        new_key = hashlib.pbkdf2_hmac('sha256', str(pin).encode('utf-8'), b64decode(salt_from_pin.encode('utf-8')), 100000)
        if b64decode(key_from_pin.encode('utf-8')) == new_key:
            ATM(card, x).login()
        else:
            print(colorama.Fore.RED,
                  '[!!] Incorrect PIN code', colorama.Style.RESET_ALL)


if __name__ == '__main__':
    colorama.init()
    mysql = db_connect.connect_db()
    cursor = mysql.cursor()

    x = 1
    while x == 1:
        card = getpass.getpass('Please Enter your Card Number: ')
        if not fl.validate(card) or not len(str(card)) == 16:
            print(colorama.Fore.RED,
                f'[!!] Your card: {card} is not valid\n',
                colorama.Style.RESET_ALL)
        else:
            cursor.execute(f"SELECT Card_Number FROM users WHERE Card_Number={card}")

            temp = False
            if cursor.fetchone():
                temp = True
                x -= 1
            else:
                print(colorama.Fore.RED,
                    f'[!!] {card} does not exist\n', colorama.Style.RESET_ALL)

        if temp:
            cursor.execute(f"SELECT Name, PIN FROM users WHERE Card_Number={card}")
            creds = [x for x in cursor.fetchone()]

            times = 0
            while temp:
                code = int(getpass.getpass(f'Please Enter PIN code for {creds[0]}: '))
                if not len(str(code)) == 6:
                    print(colorama.Fore.RED,
                        '[!!] Your PIN code is incorrect\n', colorama.Style.RESET_ALL)
                    times += 1
                    if times >= 3:
                        print(colorama.Fore.RED,
                            f'[!!] Too many PIN code retries.', colorama.Style.RESET_ALL)
                        quit()
                elif verify(code) in creds:
                    temp = False
