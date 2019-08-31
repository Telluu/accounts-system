import os
import sys
import time
import json
from getpass import getpass
from cryptography.fernet import Fernet


# TODO: Account block after 3 failed login attempts


def main():

    with open('key.key') as file:
        key = file.read()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print('1. Login')
        print('2. Register')

        option = input('\nOption: ')

        # Login
        if option == '1':
            login = input('\nLogin: ')
            password = getpass()

            accounts = request_db()

            if login in accounts and password == decrypt(login, key):
                if accounts.get(login).get('blocked') == 'false':
                    print('Login successful.')
                    time.sleep(2)

                    # Logged in phase
                    while True:
                        os.system('cls' if os.name == 'nt' else 'clear')

                        print(f'Welcome {login}!\n')
                        print('1. Change password')
                        print('2. Log-out')
                        print('3. Delete account')

                        option = input('\nOption: ')

                        # Password changing
                        if option == '1':
                            old_password = getpass('\nOld password: ')
                            new_password = getpass('\nNew password: ')
                            compare_new_password = getpass(
                                'Repeat new password: ')

                            accounts = request_db()

                            if decrypt(login, key) == old_password:
                                if new_password == compare_new_password:
                                    new_password = encrypt(new_password, key)
                                    change_password(login, new_password)
                                    print('Password changed!')
                                else:
                                    print('New passwords do not match!')
                            else:
                                print('Old password is incorrect!')

                        if option == '2':
                            print('\nLoggin-out!')
                            break

                        if option == '3':
                            password = getpass(
                                '\nType your password to delete account: ')

                            accounts = request_db()

                            if password == decrypt(login, key):
                                delete_account(login)
                                print('Account deleted!')
                                break
                            else:
                                print('Wrong password!')

                        time.sleep(2)
                else:
                    print('Your account is blocked!')
            else:
                print('Login or password is incorrect!')

        # Account creation
        elif option == '2':
            login = input('\nLogin: ')
            password = getpass('Password: ')
            compare_password = getpass('Repeat password: ')

            accounts = request_db()

            if login not in accounts and password == compare_password:
                password = encrypt(password, key)
                create_account(login, password)
                print('Account created successfully!')
            elif login in accounts:
                print('This login is already taken!')
            elif password != compare_password:
                print('Passwords do not match!')

        time.sleep(2)


def create_account(login, password):
    with open('accounts.json', 'r+') as accounts:
        data = json.load(accounts)
        data[login] = {'password': password, 'blocked': 'false'}
        accounts.seek(0)
        json.dump(data, accounts, indent=2)
        accounts.truncate()


def change_password(login, new_password):
    with open('accounts.json', 'r+') as accounts:
        data = json.load(accounts)
        data[login]['password'] = new_password
        accounts.seek(0)
        json.dump(data, accounts, indent=2)
        accounts.truncate()


def delete_account(login):
    with open('accounts.json', 'r+') as accounts:
        data = json.load(accounts)
        del data[login]
        accounts.seek(0)
        json.dump(data, accounts, indent=2)
        accounts.truncate()


def encrypt(password, key):
    f = Fernet(key)

    encrypted = f.encrypt(password.encode())
    return encrypted.decode()


def decrypt(login, key):
    f = Fernet(key)

    with open('accounts.json') as accounts:
        accounts = json.load(accounts)
        password = accounts.get(login).get('password')

    decrypted = f.decrypt(password.encode())
    return decrypted.decode()


def request_db():
    with open('accounts.json') as accounts:
        accounts = json.load(accounts)

    return accounts


main()
