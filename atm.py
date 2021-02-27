import db_connect, mysql.connector as connectSQL
import colorama, getpass, fast_luhn as fl


#TODO: develop the damn atm
class ATM:

    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin


    def login(self):
        cursor.execute(f'SELECT Name FROM users WHERE Card_Number={self.card_number}')
        results = cursor.fetchone()
        
        for result in results:
            print(colorama.Fore.GREEN,
                f'[*] Welcome, {result}!', colorama.Style.RESET_ALL)


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
                x =- 1
            else:
                print(colorama.Fore.RED,
                    f'[!!] {card} does not exist\n', colorama.Style.RESET_ALL)
        
        if temp:
            cursor.execute(f"SELECT Name, PIN FROM users WHERE Card_Number={card}")
            creds = [x for x in cursor.fetchone()]
            
            while temp:
                code = int(getpass.getpass(f'Please Enter PIN code for {creds[0]}: '))
                if not len(str(code)) == 6 or code != creds[1]:
                    print(colorama.Fore.RED,
                        '[!!] Your PIN code is incorrect\n', colorama.Style.RESET_ALL)
                elif code in creds:
                    temp = False
                    ATM(card, code).login()