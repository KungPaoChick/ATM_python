from getpass import getpass
import colorama
from base64 import b64decode
import hashlib


class my_actions:

    def Check_Balance(self, cursor, card, pin):
        auth = int(getpass('Please Enter PIN code again to confirm: '))

        if my_actions().confirm_pin(auth, pin):
            cursor.execute(f'SELECT Balance FROM users WHERE Card_Number={card}')
            for balance in cursor.fetchone():
                print(colorama.Fore.YELLOW,
                    '[*] Your current Balance is: {:,}'.format(balance), colorama.Style.RESET_ALL)
                if balance == 0:
                    cursor.execute(f'SELECT Name FROM users WHERE Card_Number={card}')
                    for name in cursor.fetchone():
                        for x in name.split()[:-1]:
                            print(f"You're broke, {x}")


    def Withdraw(self, amount, cursor, sql, card, pin):
        try:
            while True:
                conf = str(input('Continue?(y/n) '))

                if conf == '':
                    continue
                else:
                    break
            if conf.casefold() == 'y' or conf.casefold() == 'yes':
                auth = int(getpass('Please Enter PIN code again to confirm: '))

                if my_actions().confirm_pin(auth, pin):
                    cursor.execute(f'SELECT `Balance` FROM users WHERE Card_Number={card}')
                    for x in cursor.fetchone():
                        if x < amount:
                            print(colorama.Fore.RED,
                                f'[!!] Unable to Withdraw amount. {amount} exceeds your current Balance.',
                                colorama.Style.RESET_ALL)
                        elif x > amount:
                            cursor.execute(f'UPDATE `users` SET `Balance` = `Balance` - {amount} WHERE `Card_Number`={card}')
                            sql.commit()

                            cursor.execute(f'SELECT `Balance` FROM users WHERE Card_Number={card}')
                            for result in cursor.fetchone():
                                print(colorama.Fore.GREEN,
                                    '[*] Successfully Withdrawn amount. Your new Balance is: {:,}'.format(result),
                                    colorama.Style.RESET_ALL)
                        elif x == amount:
                            conf_bankrupt = str(input('Are you sure you want to withdraw all balance?(y/n) '))
                            if conf_bankrupt == 'y' or conf_bankrupt == 'yes':
                                cursor.execute(f'UPDATE `users` SET `Balance` = `Balance` - {amount} WHERE `Card_Number`={card}')
                                sql.commit()

                                cursor.execute(f'SELECT `Balance` FROM users WHERE Card_Number={card}')
                                for x in cursor.fetchone():
                                    print(colorama.Fore.GREEN,
                                        '[*] Successfully Withdrawn all Balance. Your current Balance is now: {:,}'.format(x),
                                        colorama.Style.RESET_ALL)
            elif conf.casefold() == 'n' or conf.casefold() == 'no':
                print(colorama.Fore.RED,
                    '[!!] Aborting!', colorama.Style.RESET_ALL)
        except ValueError as valerr:
            if not len(conf.casefold()) == 1 or not len(conf.casefold()) == 3:
                print(colorama.Fore.RED,
                    f'[!!] Input does not match with required length. {valerr}',
                    colorama.Style.RESET_ALL)
            else:
                print(colorama.Fore.RED,
                    f'[!!] Invalid answer. {valerr}', colorama.Style.RESET_ALL)


    def Deposit(self, amount, cursor, sql, card, pin):
        try:
            while True:
                conf = str(input('Continue?(y/n) '))

                if conf == '':
                    continue
                else:
                    break
            if conf.casefold() == 'y' or conf.casefold() == 'yes':
                auth = int(getpass('Please Enter PIN code again to confirm: '))

                if my_actions().confirm_pin(auth, pin):
                        cursor.execute(f'UPDATE `users` SET `Balance` = `Balance` + {amount} WHERE `Card_Number`={card}')
                        sql.commit()

                        cursor.execute(f'SELECT `Balance` FROM users WHERE Card_Number={card}')
                        for result in cursor.fetchone():
                            print(colorama.Fore.GREEN,
                                '[*] Successfully Deposited amount. Your new Balance is: {:,}'.format(result),
                                colorama.Style.RESET_ALL)
            elif conf.casefold() == 'n' or conf.casefold() == 'no':
                    print(colorama.Fore.RED,
                        '[!!] Aborting!', colorama.Style.RESET_ALL)
        except ValueError as valerr:
            if not len(conf.casefold()) == 1 or not len(conf.casefold()) == 3:
                print(colorama.Fore.RED,
                    f'[!!] Input does not match with required length. {valerr}',
                    colorama.Style.RESET_ALL)
            else:
                print(colorama.Fore.RED,
                    f'[!!] Invalid answer. {valerr}', colorama.Style.RESET_ALL)


    def confirm_pin(self, confirm, pin):
        salt_from_pin = pin[:88]
        key_from_pin = pin[88:]

        new_key = hashlib.pbkdf2_hmac('sha256', str(confirm).encode('utf-8'), b64decode(salt_from_pin.encode('utf-8')), 100000)
        if b64decode(key_from_pin.encode('utf-8')) == new_key:
            print(colorama.Fore.GREEN,
                '[*] Confirmed', colorama.Style.RESET_ALL)
            return True
        else:
            print(colorama.Fore.RED,
                f'[!!] {confirm} is not your PIN code.', colorama.Style.RESET_ALL)


def action(my_data):
    if my_data[0] == 1:
        my_actions().Check_Balance(my_data[1], my_data[3], my_data[4])
    elif my_data[0] == 2:
        my_data[1].execute(f'SELECT Balance FROM users WHERE Card_Number={my_data[3]}')
        for bal in my_data[1].fetchone():
            if bal == 0:
                print(colorama.Fore.RED,
                    f"[!!] You can't Withdraw, your balance is: {bal}",
                    colorama.Style.RESET_ALL)
            else:
                withdraw_amount = int(input('Enter the amount you want to Withdraw: '))
                if withdraw_amount == 0:
                    print(colorama.Fore.RED,
                        f'[!!] {withdraw_amount} is not allowed as a Withdrawal input',
                        colorama.Style.RESET_ALL)
                else:
                    my_actions().Withdraw(withdraw_amount, my_data[1], my_data[2], my_data[3], my_data[4])
    elif my_data[0] == 3:
        deposit_amount = int(input('Enter the amount you want to Deposit: '))
        if deposit_amount == 0:
            print(colorama.Fore.RED,
                f'[!!] {deposit_amount} is not allowed as a Deposit input',
                colorama.Style.RESET_ALL)
        else:
            my_actions().Deposit(deposit_amount, my_data[1], my_data[2], my_data[3], my_data[4])
