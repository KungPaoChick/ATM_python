from getpass import getpass
import colorama


class my_actions:

    def Check_Balance(self, cursor):
        pin = int(getpass('Please Enter PIN code again to confirm: '))

        if my_actions().confirm_pin(pin, cursor):
            cursor.execute(f'SELECT Balance FROM users WHERE PIN={pin}')
            balance = cursor.fetchone()
            for x in balance:
                print(colorama.Fore.YELLOW,
                    f'[*] Your current Balance is: {x}', colorama.Style.RESET_ALL)
                if x == 0:
                    print('you gotta get a job, mate')


    def Withdraw(self, amount, cursor):
        pin = int(getpass('Please Enter PIN code again to confirm: '))
        
        if my_actions().confirm_pin(pin, cursor):
            print('yeet')


    def Deposit(self, amount, cursor):
        pin = int(getpass('Please Enter PIN code again to confirm: '))
        
        if my_actions().confirm_pin(pin, cursor):
            print('yeet')


    def confirm_pin(self, confirm, cursor):
        cursor.execute(f'SELECT PIN FROM users WHERE PIN={confirm}')
        for result in cursor.fetchone():
            if confirm == result:
                print(colorama.Fore.GREEN,
                    'Confirmed', colorama.Style.RESET_ALL)
                return True
            else:
                return False


def action(my_data):
    cursor = my_data[1]
    selection = my_data[0]

    if selection == 1:
        my_actions().Check_Balance(cursor)
    elif selection == 2:
        withdraw_amount = int(input('Enter the amount you want to Withdraw: '))
        my_actions().Withdraw(withdraw_amount, cursor)
    elif selection == 3:
        deposit_amount = int(input('Enter the amount you want to Deposit: '))
        my_actions().Deposit(deposit_amount, cursor)
