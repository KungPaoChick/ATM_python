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


    def Withdraw(self, amount, cursor, sql):
        pin = int(getpass('Please Enter PIN code again to confirm: '))
        
        if my_actions().confirm_pin(pin, cursor):
            cursor.execute(f'SELECT `Balance` FROM users WHERE PIN={pin}')
            for x in cursor.fetchone():
                if x < amount:
                    print(colorama.Fore.RED,
                        f'[!!] Unable to Withdraw amount. {amount} exceeds your current Balance.',
                        colorama.Style.RESET_ALL)
                elif x > amount:
                    cursor.execute(f'UPDATE `users` SET `Balance` = `Balance` - {amount} WHERE `PIN`={pin}')
                    sql.commit()

                    cursor.execute(f'SELECT `Balance` FROM users WHERE PIN={pin}')
                    for result in cursor.fetchone():
                        print(colorama.Fore.GREEN,
                            f'[*] Successfully Withdrawn amount. Your new Balance is: {result}',
                            colorama.Style.RESET_ALL)


    def Deposit(self, amount, cursor, sql):
        pin = int(getpass('Please Enter PIN code again to confirm: '))
        
        if my_actions().confirm_pin(pin, cursor):
                cursor.execute(f'UPDATE `users` SET `Balance` = `Balance` + {amount} WHERE `PIN`={pin}')
                sql.commit()

                cursor.execute(f'SELECT `Balance` FROM users WHERE PIN={pin}') 
                for result in cursor.fetchone():
                    print(colorama.Fore.GREEN,
                        f'[*] Successfully Deposited amount. Your new Balance is: {result}',
                        colorama.Style.RESET_ALL)


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
    selection = my_data[0]
    cursor = my_data[1]
    mysql = my_data[2]

    if selection == 1:
        my_actions().Check_Balance(cursor)
    elif selection == 2:
        withdraw_amount = int(input('Enter the amount you want to Withdraw: '))
        my_actions().Withdraw(withdraw_amount, cursor, mysql)
    elif selection == 3:
        deposit_amount = int(input('Enter the amount you want to Deposit: '))
        my_actions().Deposit(deposit_amount, cursor, mysql)
