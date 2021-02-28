import colorama, string, fast_luhn as fl
import db_connect, getpass, random

class User:

    def __init__(self, account_number, card_number, cvv, name, pin):
        self.account_number = account_number
        self.card_number = card_number
        self.cvv = cvv
        self.name = name
        self.pin = pin


    def submit_user(self):
        sql = '''INSERT INTO users 
                    (Account_Number, Card_Number, CVV, Name, PIN, Balance)
                    VALUES(%s,%s,%s,%s,%s,%s)'''
        info = [self.account_number, self.card_number, self.cvv, self.name, self.pin, 0]
        db_connect.insertData(db_connect.connect_db(), info, sql)


def name_user():
    while True:
        fname = input('Please enter first name: ')
        lname = input('Please enter last name: ')
        name = f'{fname.capitalize()} {lname.capitalize()}'
        
        for letter in name:
            if letter in [char for char in string.punctuation]:
                print(colorama.Fore.RED,
                    '[!!] No Special Characters, please\n', colorama.Style.RESET_ALL)
            elif letter in [num for num in string.digits]:
                print(colorama.Fore.RED,
                    '[!!] No numbers, please\n', colorama.Style.RESET_ALL)

        if len(name) <= 3:
            print(colorama.Fore.RED,
                '[!!] Enter a valid name\n', colorama.Style.RESET_ALL)
        elif len(name) >= 30:
            print(colorama.Fore.RED,
                '[!!] Name Exceeded in length\n', colorama.Style.RESET_ALL)

        chk_name = str(input(f'{name} is your name?(y/n) '))
        if chk_name == 'y' or chk_name == 'yes':
            print(colorama.Fore.GREEN,
                f'[*] {name} has been successfully recorded\n\n', colorama.Style.RESET_ALL)
            return name
        else:
            print(colorama.Fore.RED, '[!!] Abort!', colorama.Style.RESET_ALL)


def pin_user():
    print(colorama.Fore.YELLOW,
        'PIN should be at a length of 6 numbers', colorama.Style.RESET_ALL)

    while True:
        pin = getpass.getpass('Enter new PIN: ')
        chk_pin = getpass.getpass('Enter PIN again: ')
        if pin != chk_pin:
            print(colorama.Fore.RED,
                '[!!] PIN code does not match. Try again', colorama.Style.RESET_ALL)
        elif not len(str(pin)) == 6 or not len(str(chk_pin)) == 6:
            print(colorama.Fore.RED,
                '[!!] PIN code does not match with the length of 6. Try again', colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.GREEN,
                '[*] PIN code has been successfully recorded', colorama.Style.RESET_ALL)
            return pin


def account_number_user():
    while True:
        acc_num = random.randint(100000000,999999999)
        if not len(str(acc_num)) == 9:
            continue
        else:
            return acc_num


def card_number_user():
    card = fl.generate(16)
    if fl.validate(card) and len(str(card)) == 16:
        return card


def cvv_user():
    while True:
        cvv = random.randint(100, 999)
        if not len(str(cvv)) == 3:
            continue
        else:
            return cvv


if __name__ == '__main__':
    colorama.init()
    User(account_number_user(),
         card_number_user(),
         cvv_user(),
         name_user(),
         pin_user()).submit_user()
