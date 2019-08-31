import os
import sys
import time
import string
import json
from getpass import getpass
from cryptography.fernet import Fernet


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
            pwd = getpass()

            if login in accounts() and pwd == decrpyt_pwd(login, key):
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
                        pwd = getpass('\nOld password: ')
                        new_pwd = getpass('\nNew password: ')
                        c_new_pwd = getpass('Repeat new password: ')

                        if pwd == decrpyt_pwd(login, key) and new_pwd == c_new_pwd:
                            change_password(login, new_pwd, key)
                            print('\nPassword changed!')
                        elif new_pwd == c_new_pwd:
                            print('\nNew passwords do not match!')
                        elif decrpyt_pwd(login, key) == pwd:
                            print('\nOld password is incorrect!')
                        time.sleep(2)

                    if option == '2':
                        break

                    if option == '3':
                        pwd = getpass('\nEnter password to delete account: ')
                        if pwd == decrpyt_pwd(login, key):
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
                '\nLogin (min. 4 characters and no spaces or special chars): ')
            pwd = getpass('Password (min. 6 characters and no spaces): ')
            c_pwd = getpass('Repeat password: ')

            if login not in accounts() and pwd == c_pwd:
                if len(login) < 4:
                    print('Login is too short (min. 4 characters)')
                elif len(pwd) < 6:
                    print('Password is too short')
                elif any(char in string.punctuation for char in login):
                    print('No special characters allowed in login!')
                elif any(char in string.whitespace for char in login + pwd):
                    print('No spaces allowed in login or password!')
                else:
                    create_account(login, pwd, key)
                    print('Account created successfully!')
            elif login in accounts():
                print('This login is already taken!')
            elif pwd != c_pwd:
                print('Passwords do not match!')

            time.sleep(2)


def create_account(login, pwd, key):
    f = Fernet(key)
    encrypted = f.encrypt(pwd.encode())
    pwd = encrypted.decode()

    with open('accounts.json', 'r+') as accounts:
        data = json.load(accounts)
        data[login] = pwd
        accounts.seek(0)
        json.dump(data, accounts, indent=2)
        accounts.truncate()


def change_password(login, new_pwd, key):
    f = Fernet(key)
    encrypted = f.encrypt(new_pwd.encode())
    new_pwd = encrypted.decode()

    with open('accounts.json', 'r+') as accounts:
        data = json.load(accounts)
        data[login] = new_pwd
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


def accounts():
    with open('accounts.json') as accounts:
        accounts = json.load(accounts)

    return accounts


def decrpyt_pwd(login, key):
    f = Fernet(key)

    with open('accounts.json') as accounts:
        accounts = json.load(accounts)
        encrypted = accounts.get(login)
        decrypted = f.decrypt(encrypted.encode())

    return decrypted.decode()


main()
