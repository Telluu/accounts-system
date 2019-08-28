import os
import time

# TODO: Proof-of-concept .json with accounts
# TODO: Password encryption
# TODO: Account block after 3 failed login tries

def main():

    accounts = {'root': 'toor',
                'admin': 'admin'}
    logged_in = False

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print('1. Login')
        print('2. Register')
        try:
            option = int(input('\nChoise: '))
        except ValueError:
            print('Only integers.')
            time.sleep(1)
            continue

        # Login
        if option == 1:
            login = input('\nLogin: ')
            password = input('Password: ')

            if login in accounts and password == accounts.get(login):
                logged_in = True
                print('Login successful.')
            else:
                print('Login or password is incorrect!')

        # Account creation
        if option == 2:
            login = input('\nLogin: ')
            password = input('Password: ')
            compare_password = input('Repeat password: ')

            if login not in accounts and password == compare_password:
                accounts[login] = password
                print('Account created successfully!')
            elif login in accounts:
                print('This login is already taken!')
            elif password != compare_password:
                print('Passwords do not match!')

        time.sleep(2)

        # Logged in phase
        while logged_in == True:
            os.system('cls' if os.name == 'nt' else 'clear')

            print(f'Welcome {login}!\n')
            print('1. Change password')
            print('2. Log-out')
            try:
                option = int(input('\nChoise: '))
            except ValueError:
                print('Only integers.')
                time.sleep(1)
                continue

            # Password changing
            if option == 1:
                old_password = input('\nOld password: ')
                new_password = input('\nNew password: ')
                compare_new_password = input('Repeat new password: ')

                if password == old_password and new_password == compare_new_password:
                    accounts[login] = new_password
                    print('Password changed!')
                elif password != old_password:
                    print('Old password is incorrect!')
                else:
                    print('New passwords do not match!')

            if option == 2:
                logged_in = False
                print('\nLoggin-out!')

            time.sleep(2)


main()