import colorama, string, fast_luhn as fl
import db_connect, getpass

class User:

    def __init__(self, card_number, name, pin):
        self.card_number = card_number
        self.name = name
        self.pin = pin


    def myfunc(self):
        print(f'Card Number: {self.card_number}')
        print(f'Name: {self.name}')
        print(f'PIN: {self.pin}')


    def submit_user(self):
        sql = '''INSERT INTO users (Card_Number, Name, PIN) VALUES(%s, %s, %s)'''
        info = [self.card_number, self.name, self.pin]
        db_connect.insertData(db_connect.connect_db(), info, sql)


def name_user():
    while True:
        fname = input('Please enter first name: ')
        lname = input('Please enter last name: ')
        name = f'{fname} {lname}'
        for letter in name:
            for char in string.punctuation:
                if letter == char:
                    print(colorama.Fore.RED,
                        '[!!] No Special Characters, please', colorama.Style.RESET_ALL)
                    quit()
        if len(name) <= 3:
            print(colorama.Fore.RED,
                '[!!] Enter a valid name', colorama.Style.RESET_ALL)
            quit()
        elif len(name) >= 30:
            print(colorama.Fore.RED,
                '[!!] Name Exceeded in length', colorama.Style.RESET_ALL)
            quit()

        chk_name = str(input(f'{name} is your name?(y/n) '))
        if chk_name == 'y' or chk_name == 'yes':
            print(colorama.Fore.GREEN,
                f'[*] {name} has been successfully recorded\n\n', colorama.Style.RESET_ALL)
            return values.append(name)
        else:
            print(colorama.Fore.RED, '[!!] Abort!', colorama.Style.RESET_ALL)


def pin_user():
    print(colorama.Fore.YELLOW,
        'PIN should be at a length of 6 numbers', colorama.Style.RESET_ALL)

    while True:
        pin = int(getpass.getpass('Enter new PIN: '))
        chk_pin = int(getpass.getpass('Enter PIN again: '))
        if pin != chk_pin:
            print(colorama.Fore.RED,
                '[!!] PIN code does not match. Try again', colorama.Style.RESET_ALL)
        elif not len(str(pin)) == 6 or not len(str(chk_pin)) == 6:
            print(colorama.Fore.RED,
                '[!!] PIN code does not match with the length of 6. Try again', colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.GREEN,
                '[*] PIN code has been successfully recorded', colorama.Style.RESET_ALL)
            return values.append(pin)


def card_number_user():
    card = fl.generate(16)
    if fl.validate(card):
        values.append(card)
        return card


if __name__ == '__main__':
    colorama.init()
    values = []
    card_number_user()
    name_user()
    pin_user()
    User(values[0], values[1], values[2]).myfunc()
