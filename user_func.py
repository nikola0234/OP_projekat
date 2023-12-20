# Ovaj fajl sadrzi funcije koje se koriste u radu sa korisnicima.
import os
import re
from main import main
import movie_functions
users = []
user = {}

# Funcije za validaciju korisnika


def logout():
    logged_in = False
    return logged_in


def is_valid_password(password):
    return len(password) >= 6 and bool(re.search(r'\d', password))


def is_username_taken(username, user_list):
    return any(u['username'] == username for u in user_list)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Funcije za login i register


def login(username, password):
    global user
    try:
        user = next((u for u in users if u['username'] == username))
        max_attempts = 5
        attempts = 0
        while True:
            if password == user['password']:
                print('Logged in successfully!')
                return user['role']
            else:
                clear_screen()
                print(f'Wrong password. Attempts left: {max_attempts - attempts}')
                password = input("Enter your password: ")
                attempts += 1
                if attempts == max_attempts:
                    clear_screen()
                    print("Maximum login attempts reached. Returning to the main menu.")
                    break
    except StopIteration:
        clear_screen()
        print('Username not found.')
        return None


def register():
    while True:
        clear_screen()
        print('Welcome to registration, please enter the following: \n')
        username = input("Enter username: ")
        password = input("Enter password(min. 6 characters and 1 number): ")
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        role = 'registered_user'

        if len(password) < 6 or not re.search(r'\d', password):
            clear_screen()
            print("Password need to have at least 6 characters and one number. Try again: \n")
            input("Press enter to continue...")
            continue

        if any(username == user['username'] for user in users):
            clear_screen()
            print("Already taken username,try another one.\n")
            input("Press enter to continue...")
            continue

        user_data = {
            'username': username,
            'password': password,
            'name': name,
            'surname': surname,
            'role': role + '\n'
        }
        users.append(user_data)
        with open('users1.txt', "+a") as fin:
            fin.write(user_data['username'] + '|' + user_data['password'] + '|' + user_data['name'] + '|' + user_data[
                'surname'] + '|' + user_data['role'])
        clear_screen()
        print('Succesefully registered!')
        return

# Funcije za menije za menadzere, prodavce i obicne korisnike.


def manager_menu(logged_in):
    clear_screen()

    def new_employee():
        print('Enter the data for new employee... \n ')
        username = input('Enter the username: ')
        name = input('Enter the name: ')
        surname = input('Enter the surname: ')
        password = input('Enter the password: ')
        role = 'employee'

        if is_valid_password(password) and not is_username_taken(username, users):
            user_data = {
                'username': username,
                'password': password,
                'name': name,
                'surname': surname,
                'role': role+'\n'
            }
            users.append(user_data)
            with open('users1.txt', "+a") as fin:
                fin.write(
                    user_data['username'] + '|' + user_data['password'] + '|' + user_data['name'] + '|' + user_data[
                        'surname'] + '|' + user_data['role'])
            print('\nNew employee successfully added!')
            input('Enter to continue...')
            clear_screen()
            return
        elif is_username_taken(username, users):
            clear_screen()
            print('Already taken username,try another one.\n')
            new_employee()

        else:
            clear_screen()
            print('Password need to have at least 6 characters and one number. Try again: \n')
            new_employee()

    def new_manager():
        print('Enter the data for new manager... \n ')
        username = input('Enter the username: ')
        name = input('Enter the name: ')
        surname = input('Enter the surname: ')
        password = input('Enter the password: ')
        role = 'manager'

        if is_valid_password(password):
            user_data = {
                'username': username,
                'password': password,
                'name': name,
                'surname': surname,
                'role': role+'\n'
            }
            users.append(user_data)
            with open('users1.txt', "+a") as fin:
                fin.write(
                    user_data['username'] + '|' + user_data['password'] + '|' + user_data['name'] + '|' + user_data[
                        'surname'] + '|' + user_data['role'])
            print('\nNew manager successfully added!')
            input('Enter to continue...')
            clear_screen()
            return
        else:
            clear_screen()
            print('Password need to have at least 6 characters and one number. Try again: \n')
            new_manager()

    while logged_in:
        print('Welcome to manager menu.\n')
        print('1. Logging out')
        print('2. Change your personal data')
        print('3. Add new employee')
        print('4. Add new manager')
        print('5. List of avaliable movies')
        print('6. Search for movies')
        print('7. Add new movie')
        print('8. Delete movie')
        print('9. Change the movie data')
        print('10. Add new movie projection')
        print('11. Delete movie projection')
        print('12. Quit the app')
        choice = input('Enter your choice: ')
        if choice == '1':
            logged_in = False
            main()
        elif choice == '2':
            change_data(user)
        elif choice == '3':
            clear_screen()
            new_employee()
        elif choice == '4':
            clear_screen()
            new_manager()
        elif choice == '5':
            clear_screen()
            movie_functions.avaliable_movies()
        elif choice == '6':
            clear_screen()
            movie_functions.search_movie()
        elif choice == '7':
            clear_screen()
            movie_functions.add_new_movie()
        elif choice == '8':
            clear_screen()
            movie_functions.delete_movie()
        elif choice == '9':
            clear_screen()
            movie_functions.change_movie_data()
        elif choice == '10':
            clear_screen()
            movie_functions.add_new_projection()
        elif choice == '11':
            clear_screen()
            movie_functions.delete_movie_projection()
        elif choice == '12':
            clear_screen()
            logged_in = False
            break
        else:
            clear_screen()
            print("Not existing choice. Try again.")


def employee_menu(logged_in):
    clear_screen()
    while logged_in:
        print('Welcome to employee menu.\n')
        print('1. Logging out')
        print('2. Change your personal data')
        print('3. List of avaliable movies')
        print('4. Search for movies')
        print('5. Quit the app')
        choice = input('Enter your choice: ')
        if choice == '1':
            logged_in = False
            main()
        elif choice == '2':
            change_data(user)
        elif choice == '3':
            clear_screen()
            movie_functions.avaliable_movies()
        elif choice == '4':
            clear_screen()
            movie_functions.search_movie()
        elif choice == '5':
            clear_screen()
            return
        else:
            clear_screen()
            print("Not existing choice. Try again.")


def user_menu(logged_in):
    clear_screen()
    while logged_in:
        print('Welcome to user menu.\n')
        print('1. Logging out')
        print('2. Change your personal data')
        print('3. List of avaliable movies')
        print('4. Search for movies')
        print('5. Quit the app')
        choice = input('Enter your choice: ')
        if choice == '1':
            logged_in = False
            main()
        elif choice == '2':
            change_data(user)
        elif choice == '3':
            clear_screen()
            movie_functions.avaliable_movies()
        elif choice == '4':
            clear_screen()
            movie_functions.search_movie()
        elif choice == '5':
            clear_screen()
            break
        else:
            clear_screen()
            print("Not existing choice. Try again.")


def change_data(user1):
    clear_screen()
    print(f"Your current data is:\n"    
      f"\tname: {user1['name']}\n"    
      f"\tsurname: {user1['surname']}\n"
      f"\tpassword: {user1['password']}\n")

    print('What do you want to change(name,surname,password or back)? ')
    choice = input('Enter your choice here: ')
    if choice == 'name':
        new_name = input('Enter the new name: ')
        user1['name'] = new_name
        clear_screen()
        print('Data successfully changed.')
    elif choice == 'surname':
        new_surname = input('Enter the new surname: ')
        user1['surname'] = new_surname
        clear_screen()
        print('Data successfully changed.')
    elif choice == 'password':
        new_password = input('Enter the new password: ')
        if len(new_password)<6 or not re.search(r'\d', new_password):
            clear_screen()
            print("Password need to have at least 6 characters and one number. Try again: \n")
            input("Press enter to continue... ")
            change_data(user1)
        else:
            user1['password'] = new_password
        clear_screen()
        print('Data successfully changed. ')
    elif choice == 'back':
        clear_screen()
        return
    else:
        clear_screen()
        print('This choise does not exist, try again...')
        input('Enter to continue...')
        change_data(user1)
    for u in users:
        if u['username'] == user1['username']:
            u['name'] = user1['name']
            u['surname'] = user1['surname']
            u['password'] = user1['password']
    with open('users1.txt', 'w') as fin:
        for u in users:
            fin.write(u['username']+'|' + u['password']+'|' + u['name'] + '|' + u['surname'] + '|' + u['role'])

# Funcija za iscitavanje podataka o korisnicima


def read_user_data():
    with open('users1.txt', 'r') as fin:
        for line in fin:
            a = line.split('|')
            useer_to_read = {
                'username': a[0],
                'password': a[1],
                'name': a[2],
                'surname': a[3],
                'role': a[4]
            }
            users.append(useer_to_read)


def write_users_to_file(users1):
    with open('users1.txt', 'w') as file:
        for data in users1:
            values = data['username'], data['password'], data['name'], data['surname'], data['role']
        for user_data in values:
            line = '|'.join(user_data)
            file.write(line + '\n')


