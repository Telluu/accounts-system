#!/usr/bin/env python3

import os
import time
import string
import json
from getpass import getpass
import hashlib
import binascii


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

            # Checking credentials
            if login in users() and verify_password(login, pwd) == True:
                # Logged in phase
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f'Welcome {login}!\n')
                    print('1. Log-out')
                    print('2. Change password')
                    print('3. Delete account')
                    option = input('\nOption: ')

                    # Log-out
                    if option == '1':
                        break

                    # Password changing
                    if option == '2':
                        pwd = getpass('\nOld password: ')
                        new_pwd = getpass('\nNew password: ')
                        c_new_pwd = getpass('Repeat new password: ')

                        if verify_password(login, pwd) == True and new_pwd == c_new_pwd:
                            if len(pwd) < 4:
                                print('Password is too short (min. 4 characters)')
                            elif any(char in string.whitespace for char in pwd):
                                print('No spaces allowed in password!')
                            else:
                                change_password(login, new_pwd)
                                print('\nPassword changed!')
                        elif new_pwd != c_new_pwd:
                            print('\nNew passwords do not match!')
                        elif verify_password(login, pwd) != True:
                            print('\nOld password is incorrect!')
                        time.sleep(2)

                    # Account deletion
                    if option == '3':
                        pwd = getpass('\nEnter password to delete account: ')

                        if verify_password(login, pwd) == True:
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
            login = input('\nLogin: ')
            pwd = getpass()
            c_pwd = getpass('Repeat password: ')

            if login not in users() and pwd == c_pwd:
                if len(login) < 4 or len(pwd) < 4:
                    print('Login or password is too short (min. 4 characters)')
                elif any(char in string.punctuation for char in login):
                    print('No special characters allowed in login!')
                elif any(char in string.whitespace for char in login + pwd):
                    print('No spaces allowed in login or password!')
                else:
                    create_account(login, pwd)
                    print('Account created successfully!')
            elif login in users():
                print('This login is already taken!')
            elif pwd != c_pwd:
                print('Passwords do not match!')

            time.sleep(2)


def create_account(login, password):
    password = hash_password(password)
    with open('users.json', 'r+') as users:
        data = json.load(users)
        data[login] = password
        users.seek(0)
        json.dump(data, users, indent=4)
        users.truncate()


def change_password(login, new_password):
    new_password = hash_password(new_password)
    with open('users.json', 'r+') as users:
        data = json.load(users)
        data[login] = new_password
        users.seek(0)
        json.dump(data, users, indent=4)
        users.truncate()


def delete_account(login):
    with open('users.json', 'r+') as users:
        data = json.load(users)
        del data[login]
        users.seek(0)
        json.dump(data, users, indent=4)
        users.truncate()


def users():
    with open('users.json') as users:
        users = json.load(users)

    return users


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(login, password):
    with open('users.json') as users:
        users = json.load(users)
        stored_password = users.get(login)

    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


if __name__ == '__main__':
    main()
