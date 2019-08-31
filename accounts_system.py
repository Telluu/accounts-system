import os
import sys
import time
import string
import json
from getpass import getpass
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=['pbkdf2_sha256'],
    default='pbkdf2_sha256',
    pbkdf2_sha256__default_rounds=30000)


def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print('1. Login')
        print('2. Register')

        option = input('\nOption: ')

        # Login
        if option == '1':
            login = input('\nLogin: ')
            pwd = getpass()

            if login in accounts() and verify_pwd(login, pwd) == True:
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
                        pwd = getpass('\nOld password: ')
                        new_pwd = getpass('\nNew password: ')
                        c_new_pwd = getpass('Repeat new password: ')

                        if verify_pwd(login, pwd) == True and new_pwd == c_new_pwd:
                            change_password(login, new_pwd)
                            print('\nPassword changed!')
                        elif new_pwd == c_new_pwd:
                            print('\nNew passwords do not match!')
                        elif verify_pwd(login, pwd) == True:
                            print('\nOld password is incorrect!')
                        time.sleep(2)

                    # Log-out
                    if option == '2':
                        break

                    # Account deletion
                    if option == '3':
                        pwd = getpass('\nEnter password to delete account: ')
                        if verify_pwd(login, pwd) == True:
                            delete_account(login)
                            print('Account deleted!')
                            break
                        else:
                            print('Wrong password!')
                        time.sleep(2)
            else:
                print('Login or password is incorrect!')
                time.sleep(2)

        # Account creation
        elif option == '2':
            login = input(
                '\nLogin: ')
            pwd = getpass()
            c_pwd = getpass('Repeat password: ')

            if login not in accounts() and pwd == c_pwd:
                if len(login) < 4 or len(pwd) < 4:
                    print('Login or password is too short (min. 4 characters)')
                elif any(char in string.punctuation for char in login):
                    print('No special characters allowed in login!')
                elif any(char in string.whitespace for char in login + pwd):
                    print('No spaces allowed in login or password!')
                else:
                    create_account(login, pwd)
                    print('Account created successfully!')
            elif login in accounts():
                print('This login is already taken!')
            elif pwd != c_pwd:
                print('Passwords do not match!')

            time.sleep(2)


def create_account(login, password):
    with open('accounts.json', 'r+') as accounts:
        data = json.load(accounts)
        data[login] = pwd_context.hash(password)
        accounts.seek(0)
        json.dump(data, accounts, indent=4)
        accounts.truncate()


def change_password(login, new_password):
    with open('accounts.json', 'r+') as accounts:
        data = json.load(accounts)
        data[login] = pwd_context.hash(new_password)
        accounts.seek(0)
        json.dump(data, accounts, indent=4)
        accounts.truncate()


def delete_account(login):
    with open('accounts.json', 'r+') as accounts:
        data = json.load(accounts)
        del data[login]
        accounts.seek(0)
        json.dump(data, accounts, indent=4)
        accounts.truncate()


def accounts():
    with open('accounts.json') as accounts:
        accounts = json.load(accounts)

    return accounts


def verify_pwd(login, password):
    with open('accounts.json') as accounts:
        accounts = json.load(accounts)
        hashed = accounts.get(login)

    return pwd_context.verify(password, hashed)


main()
