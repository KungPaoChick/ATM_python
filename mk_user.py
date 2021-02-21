import colorama, string, fast_luhn as fl
import db_connect

class User:

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin


    def submit_user(self):
        sql = '''INSERT INTO users (Name) VALUES(%s)'''
        db_connect.insertData(db_connect.connect_db(), self.name, sql)


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
        else:
            print(colorama.Fore.GREEN,
                f'[*] {name} has been successfully recorded\n\n', colorama.Style.RESET_ALL)
            return name


def pin_user():
    print(colorama.Fore.YELLOW,
        'PIN should be at a length of 6 numbers', colorama.Style.RESET_ALL)

    while True:
        pin = int(input('Enter new PIN: '))
        chk_pin = int(input('Enter PIN again: '))
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


if __name__ == '__main__':
    colorama.init()
    name_user()
    pin_user()
