from getpass import getpass
import colorama


class my_actions:

    def Check_Balance(self, cursor, pin):
        conf = int(getpass('Please Enter PIN code again to confirm: '))

        if my_actions().confirm_pin(conf, pin):
            cursor.execute(f'SELECT Balance FROM users WHERE PIN={conf}')
            balance = cursor.fetchone()
            for x in balance:
                print(colorama.Fore.YELLOW,
                    f'[*] Your current Balance is: {x}', colorama.Style.RESET_ALL)
                if x == 0:
                    print('you gotta get a job, mate')


    def Withdraw(self, amount, cursor, sql, pin):
        conf = int(getpass('Please Enter PIN code again to confirm: '))
        
        if my_actions().confirm_pin(conf, pin):
            cursor.execute(f'SELECT `Balance` FROM users WHERE PIN={conf}')
            for x in cursor.fetchone():
                if x < amount:
                    print(colorama.Fore.RED,
                        f'[!!] Unable to Withdraw amount. {amount} exceeds your current Balance.',
                        colorama.Style.RESET_ALL)
                elif x > amount:
                    cursor.execute(f'UPDATE `users` SET `Balance` = `Balance` - {amount} WHERE `PIN`={conf}')
                    sql.commit()

                    cursor.execute(f'SELECT `Balance` FROM users WHERE PIN={conf}')
                    for result in cursor.fetchone():
                        print(colorama.Fore.GREEN,
                            f'[*] Successfully Withdrawn amount. Your new Balance is: {result}',
                            colorama.Style.RESET_ALL)
                elif x == amount:
                    conf_bankrupt = str(input('Are you sure you want to withdraw all balance?(y/n) '))
                    if conf_bankrupt == 'y' or conf_bankrupt == 'yes':
                        cursor.execute(f'UPDATE `users` SET `Balance` = `Balance` - {amount} WHERE `PIN`={conf}')
                        sql.commit()

                        cursor.execute(f'SELECT `Balance` FROM users WHERE PIN={conf}')
                        for x in cursor.fetchone():
                            print(colorama.Fore.GREEN,
                                f'[*] Successfully Withdrawn all Balance. Your current Balance is now: {x}',
                                colorama.Style.RESET_ALL)
                    else:
                        continue


    def Deposit(self, amount, cursor, sql, pin):
        conf = int(getpass('Please Enter PIN code again to confirm: '))
        
        if my_actions().confirm_pin(conf, pin):
                cursor.execute(f'UPDATE `users` SET `Balance` = `Balance` + {amount} WHERE `PIN`={conf}')
                sql.commit()

                cursor.execute(f'SELECT `Balance` FROM users WHERE PIN={conf}') 
                for result in cursor.fetchone():
                    print(colorama.Fore.GREEN,
                        f'[*] Successfully Deposited amount. Your new Balance is: {result}',
                        colorama.Style.RESET_ALL)


    def confirm_pin(self, confirm, pin):
        if confirm == pin:
            print(colorama.Fore.GREEN,
                '[*] Confirmed', colorama.Style.RESET_ALL)
            return True
        else:
            print(colorama.Fore.RED,
                f'[!!] {confirm} is not your PIN code.', colorama.Style.RESET_ALL)


def action(my_data):
    if my_data[0] == 1:
        my_actions().Check_Balance(my_data[1], my_data[3])
    elif my_data[0] == 2:
        withdraw_amount = int(input('Enter the amount you want to Withdraw: '))
        my_actions().Withdraw(withdraw_amount, my_data[1], my_data[2], my_data[3])
    elif my_data[0] == 3:
        deposit_amount = int(input('Enter the amount you want to Deposit: '))
        my_actions().Deposit(deposit_amount, my_data[1], my_data[2], my_data[3])
