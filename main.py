import user_func
import movie_functions
import ticket_functions


def main():
    logged_in = False
    user_func.clear_screen()
    while not logged_in:
        print('Welcome to our cinema app')
        print("\n1. Login")
        print("2. Register")
        print('3. List of avaliable movies')
        print('4. Search for movie')
        print('5. Search for movie projection')
        print('6. Reserve ticket')
        print("7. Quit the app")
        choice = input('Enter your choice: ')

        if choice == '1':
            user_func.clear_screen()
            print('Logging in, please enter the following data: \n')
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user_role = user_func.login(username, password)
            if user_role:
                logged_in = True
                if user_role == 'manager\n':
                    user_func.manager_menu(logged_in)
                elif user_role == 'employee\n':
                    user_func.employee_menu(logged_in)
                elif user_role == 'registered_user\n':
                    user_func.user_menu(logged_in)
        elif choice == '2':
            user_func.register()
        elif choice == '3':
            user_func.clear_screen()
            movie_functions.avaliable_movies()
        elif choice == '4':
            user_func.clear_screen()
            movie_functions.search_movie()
        elif choice == '5':
            user_func.clear_screen()
            movie_functions.search_projection()
        elif choice == '6':
            user_func.clear_screen()
            ticket_functions.reserving_tickets(False)
        elif choice == '7':
            user_func.clear_screen()
            break
        else:
            user_func.clear_screen()
            print("Not existing choice. Try again.")


if __name__ == '__main__':
    user_func.read_user_data()
    movie_functions.read_movies()
    movie_functions.read_projections()
    movie_functions.read_cinema_hall()
    movie_functions.generate_appointments_from_projections()
    movie_functions.read_appointment()
    movie_functions.delete_appointments_after_date_pass()
    ticket_functions.read_tickets()
    ticket_functions.read_halls()
    ticket_functions.generate_seats_for_appointment()
    ticket_functions.read_seats_for_appointment()
    ticket_functions.read_loyalty_cards()
    ticket_functions.read_sold_tickets_info()
    ticket_functions.read_appointment_info()
    ticket_functions.read_user_for_tickets()
    main()
