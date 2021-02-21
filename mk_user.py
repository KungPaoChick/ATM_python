import colorama, fast_luhn as fl
from string import punctuation
import db_connect

class User:

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin


    def submit_user(self, name, pin):
        db_connect.insertData(db_connect.connect_db(), name)


def name_user():
    fname = input('Please enter first name: ')
    lname = input('Please enter last name: ')
    name = f'{fname} {lname}'
    for letter in name:
        for char in punctuation:
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
            f'[*] {name} has been successfully recorded', colorama.Style.RESET_ALL)
        return name


if __name__ == '__main__':
    colorama.init()
    print(name_user())