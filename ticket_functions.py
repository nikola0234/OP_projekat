import movie_functions
import validations
from movie_functions import projections
from movie_functions import apointments
import datetime
import tabulate

tickets_reserved = []
tickets_sold = []
tickets_canceled = []
seats_for_appointment = []
halls = []


def read_tickets():
    with open('tickets.txt', 'r') as fin:
        for line in fin:
            ticket_data = line.split('|')
            ticket = {
                'name': ticket_data[0],
                'appointment': ticket_data[1],
                'seat': ticket_data[2],
                'date_sold': ticket_data[3],
                'status': ticket_data[4]
            }
            if 'reserved' in ticket['status']:
                tickets_reserved.append(ticket)
            elif 'sold' in ticket['status']:
                tickets_sold.append(ticket)
            elif 'canceled' in ticket['status']:
                tickets_canceled.append(ticket)


def write_tickets():
    with open('tickets.txt', 'w') as fin:
        for reserved in tickets_reserved:
            fin.write(
                reserved['name'] + '|' +
                reserved['appointment'] + '|' +
                reserved['seat'] + '|' +
                reserved['date_sold'] + '|' +
                reserved['status']
            )

        for sold in tickets_sold:
            fin.write(
                sold['name'] + '|' +
                sold['appointment'] + '|' +
                sold['seat'] + '|' +
                sold['date_sold'] + '|' +
                sold['status']
            )

        for canceled in tickets_canceled:
            fin.write(
                canceled['name'] + '|' +
                canceled['appointment'] + '|' +
                canceled['seat'] + '|' +
                canceled['date_sold'] + '|' +
                canceled['status']
            )


def read_halls():
    with open('cinema_halls.txt', 'r') as fin:
        for line in fin:
            hall_data = line.split('|')
            hall = {
                'name': hall_data[0],
                'rows': hall_data[1],
                'columns': hall_data[2],
                'status': hall_data[3]
            }

            halls.append(hall)


def read_seats_for_appointment():
    with open('appointment_seats.txt', 'r') as fin:
        for line in fin:
            seats_data = line.split('|')
            data = {
                'code': seats_data[0],
                'seats': seats_data[1],
            }

            seats_for_appointment.append(data)


def write_seats_for_appointment():
    with open('appointment_seats.txt', 'w') as fin:
        for data in seats_for_appointment:
            fin.write(
                data['code'] + '|' +
                data['seats']
            )


def search_for_date_of_appointment(code):
    for appointment in apointments:
        if code == appointment['code']:
            return appointment['date']


def generate_seats_for_appointment():
    active_appointment_codes = []
    active_appointment_halls = []
    existing_codes = []
    with open('projection_appointment.txt', 'r') as fin:
        for app in fin:
            app_data = app.split('|')
            if 'active' in app_data[3]:
                active_appointment_codes.append(app_data[0])
                active_appointment_halls.append(app_data[2])
    with open('appointment_seats.txt', 'r') as fin:
        for app in fin:
            app_data = app.split('|')
            existing_codes.append(app_data[0])

    data_to_write = []
    for code, hall in zip(active_appointment_codes, active_appointment_halls):
        for hall_info in halls:
            if hall in hall_info['name']:
                rows = [chr(j) for j in range(ord('a'), ord('a') + int(hall_info['rows']))]
                columns = [str(j) for j in range(1, 1 + int(hall_info['columns']))]

                seat_str = ','.join([f"{row}{column}" for row in rows for column in columns])

                appointments_seats = f"{code}|{seat_str}"

                if code not in existing_codes:
                    data_to_write.append(appointments_seats)

    with open('appointment_seats.txt', 'a') as fout:
        for data in data_to_write:
            fout.write(data + '\n')
    print(seats_for_appointment)


def print_reserved_tickets_user(user):
    headers = ["#", "Appointment code", "Movie name", "Date of appointment", "Starting time", "Ending time", "Seat" ]
    table_data = []
    num = 1
    for ticket in tickets_reserved:
        for projection in projections:
            if ticket['name'] == user['username']:
                if projection['code'] in ticket['appointment']:
                    app_date = search_for_date_of_appointment(ticket['appointment'])
                    table_row = [
                        num,
                        ticket['appointment'],
                        projection['movie name'],
                        app_date,
                        projection['starting time'],
                        projection['ending time'],
                        ticket['seat']
                    ]
                    if 'reserved' in ticket['status']:
                        table_data.append(table_row)
                        num += 1
    table = tabulate.tabulate(table_data, headers= headers, tablefmt= "grid")
    print(table)


def print_reserved_tickets_employee(reserved, sold):
    headers = ["#", "Appointment code", "Username/Name and surname", "Movie name", "Date of appointment", "Starting time", "Ending time", "Seat", "Ticket status"]
    table_data = []
    num = 1
    for ticket_r in reserved:
        for projection in projections:
            if projection['code'] in ticket_r['appointment']:
                app_date = search_for_date_of_appointment(ticket_r['appointment'])
                table_row = [
                    num,
                    ticket_r['appointment'],
                    ticket_r['name'],
                    projection['movie name'],
                    app_date,
                    projection['starting time'],
                    projection['ending time'],
                    ticket_r['seat'],
                    ticket_r['status']
                ]

                if 'reserved' in ticket_r['status'] or 'sold' in ticket_r['status']:
                    table_data.append(table_row)
                    num += 1
    for ticket_s in sold:
        for projection in projections:
            if projection['code'] in ticket_s['appointment']:
                app_date = search_for_date_of_appointment(ticket_s['appointment'])
                table_row = [
                    num,
                    ticket_s['appointment'],
                    ticket_s['name'],
                    projection['movie name'],
                    app_date,
                    projection['starting time'],
                    projection['ending time'],
                    ticket_s['seat'],
                    ticket_s['status']
                ]

                if 'reserved' in ticket_s['status'] or 'sold' in ticket_s['status']:
                    table_data.append(table_row)
                    num += 1
    table = tabulate.tabulate(table_data, headers= headers, tablefmt= "grid")
    print(table)


def print_seats(movie_code):
    hall_name = None
    num_columns = None
    num_rows = None
    input_string = None
    for app in seats_for_appointment:
        if app['code'] == movie_code:
            input_string = app['seats']

    for app in apointments:
        if app['code'] == movie_code:
            hall_name = app['hall']

    for hall in halls:
        if hall_name in hall['name']:
            num_rows = int(hall['columns'])
            num_columns = int(hall['rows'])
    matrix = [[None for _ in range(num_columns)] for _ in range(num_rows)]
    elements = input_string.split(',')
    for i in range(num_rows):
        for j in range(num_columns):
            matrix[i][j] = elements[j * num_rows + i]
    for row in matrix:
        print("|".join(row))


def reserving_tickets(user):
    seats = None
    name_surname = None
    existing_app_codes = []
    for code in apointments:
        if code['status'] == 'active\n':
            existing_app_codes.append(code['code'])
    if not user:
        while True:
            name_surname = input('You are not registered, please enter name and surname for your ticket reservation: ')
            if not name_surname:
                print('Name or surname must include at least one character. Please try again.')
            else:
                break
    if user and user['role'] == 'employee\n':
        while True:
            name_surname = input('Enter name and surname for unregistered user or username for registered user: ')
            if not name_surname:
                print('Name or surname must include at least one character. Please try again.')
            else:
                break
    while True:
        movie_functions.print_table_projection(projections, apointments)
        print('Enter the code of appointment of movie projection you want to buy ticket for(x to go back) ')
        while True:
            ticket_code = input('Enter the code here: ')
            if ticket_code.lower() == 'x':
                break
            if ticket_code not in existing_app_codes:
                print(existing_app_codes)
                print('Entered code not in existing appointments. Try again')
            else:
                break
        if ticket_code.lower() == 'x':
            break
        for i in seats_for_appointment:
            if ticket_code in i['code']:
                seats = i['seats'].split(',')
        while True:
            print_seats(ticket_code)
            print(seats)
            chosen_seat = input('Choose one of best free seats for you: ')
            if chosen_seat not in seats:
                print('You entered filled or not existing seat, please try again.')
            else:
                break
        for i, seat in enumerate(seats):
            if seat == chosen_seat:
                seats[i] = 'X'

        result_seats = ','.join(seats)
        for i in seats_for_appointment:
            if ticket_code in i['code']:
                i['seats'] = result_seats
        write_seats_for_appointment()
        if not user:
            new_ticket = {
                'name': name_surname,
                'appointment': ticket_code,
                'seat': chosen_seat,
                'date_sold': datetime.datetime.now().strftime('%d.%m.%Y'),
                'status': 'reserved\n'
            }
        if user and user['role'] != 'employee\n':
            new_ticket = {
                'name': user['username'],
                'appointment': ticket_code,
                'seat': chosen_seat,
                'date_sold':  datetime.datetime.now().strftime('%d.%m.%Y'),
                'status': 'reserved\n'
            }
        else:
            new_ticket = {
                'name': name_surname,
                'appointment': ticket_code,
                'seat': chosen_seat,
                'date_sold': datetime.datetime.now().strftime('%d.%m.%Y'),
                'status': 'reserved\n'
            }
        tickets_reserved.append(new_ticket)
        write_tickets()
        cont = input('Succesefully reserved a ticket, press enter to reserve more or press x to go back to menu: ')
        if cont.lower() == 'x':
            break


def check_reserved_tickets(user):
    while True:
        print('These are your current reserved tickets:')
        print_reserved_tickets_user(user)
        back = input('Enter x to go back: ')

        if back.lower() == 'x':
            break


def check_reserved_tickets_employee(user):
    while True:
        print('List of reserved and sold tickets:')
        print_reserved_tickets_employee(tickets_reserved, tickets_sold)
        back = input('Enter x to go back: ')

        if back.lower() == 'x':
            break


def canceling_reservation(user):
    existing_tickets = []
    seat_to_write = None
    hall_name = None
    seats_per_row = None
    for code in tickets_reserved:
        if code['name'] == user['username']:
            existing_tickets.append(code['appointment'])
    while True:
        print(existing_tickets)
        print('These are your current reserved tickets:')
        print_reserved_tickets_user(user)
        deleted = False
        while True:
            ticket_to_cancel = input('Enter the appointment code for reservation you want to cancel(x to go back): ')

            if ticket_to_cancel.lower() == 'x':
                break
            if ticket_to_cancel not in existing_tickets:
                print('There is no reservation with that code, please try again.')
            else:
                break
        if ticket_to_cancel.lower() == 'x':
            break
        while True:
            for ticket in tickets_reserved:
                if ticket['name'] == user['username'] and ticket['appointment'] == ticket_to_cancel and existing_tickets.count(ticket['appointment']) < 2 and not deleted:
                    ticket['status'] = 'canceled\n'
                    seat_to_write = ticket['seat']
                    deleted = True
                    write_tickets()
                elif ticket['name'] == user['username'] and ticket['appointment'] == ticket_to_cancel and existing_tickets.count(ticket['appointment']) >= 2 and not deleted:
                    seat_to_write = input('There are more tickets for same appointment, enter wich seat you want to cancel: ')
                    for ticket1 in tickets_reserved:
                        if ticket1['appointment'] == ticket_to_cancel and ticket1['seat'] == seat_to_write:
                            ticket1['status'] = 'canceled\n'
                            existing_tickets.remove(ticket['appointment'])
                            deleted = True
                            write_tickets()
            if deleted:
                break
            else:
                print('Entered seat is not among tickets. Try again.')
        for app in seats_for_appointment:
            if app['code'] == ticket_to_cancel:
                col, row = seat_to_write[0], seat_to_write[1:]

                col_index = ord(col) - ord('a')
                row_index = int(row)

                for appointment in apointments:
                    if app['code'] == appointment['code']:
                        hall_name = appointment['hall']

                for hall in halls:
                    if hall['name'] == hall_name:
                        seats_per_row = hall['columns']

                position = col_index * int(seats_per_row) + row_index - 1

                seats = app['seats']
                list_of_seats = seats.split(',')

                list_of_seats[position] = seat_to_write

                joined_seats = ','.join(list_of_seats)

                app['seats'] = joined_seats

                write_seats_for_appointment()

        print('Succesefully canceled a ticket.')
        deleted = False
        cont = input('Continue canceling ot X to go back to menu: ')

        if cont.lower() == 'x':
            break


def canceling_tickets_employee(user):
    existing_tickets = []

    deleted = False
    seat_to_write = None
    hall_name = None
    seats_per_row = None

    for reserved in tickets_reserved:
        existing_tickets.append(reserved['appointment'])

    for sold in tickets_sold:
        existing_tickets.append(sold['appointment'])

    while True:
        print(existing_tickets)
        print('These are tickets that you can cancel:')
        print_reserved_tickets_employee(tickets_reserved, tickets_sold)
        deleted = False
        while True:
            ticket_to_cancel = input('Enter the appointment code for reservation you want to cancel(x to go back): ')

            if ticket_to_cancel.lower() == 'x':
                break
            if ticket_to_cancel not in existing_tickets:
                print('There is no reservation with that code, please try again.')
            else:
                break
        if ticket_to_cancel.lower() == 'x':
            break

        while True:
            for ticket in tickets_reserved:
                if ticket['appointment'] == ticket_to_cancel and existing_tickets.count(ticket['appointment']) < 2 and not deleted:
                    ticket['status'] = 'canceled\n'
                    seat_to_write = ticket['seat']
                    deleted = True
                    write_tickets()
                elif ticket['appointment'] == ticket_to_cancel and existing_tickets.count(ticket['appointment']) >= 2 and not deleted:
                    seat_to_write = input('There are more tickets for same appointment, enter wich seat you want to cancel: ')
                    for ticket1 in tickets_reserved:
                        if ticket1['appointment'] == ticket_to_cancel and ticket1['seat'] == seat_to_write:
                            ticket1['status'] = 'canceled\n'
                            existing_tickets.remove(ticket['appointment'])
                            deleted = True
                            write_tickets()
            if deleted:
                break
            for ticket in tickets_sold:
                if ticket['appointment'] == ticket_to_cancel and existing_tickets.count(ticket['appointment']) < 2 and not deleted:
                    ticket['status'] = 'canceled\n'
                    seat_to_write = ticket['seat']
                    deleted = True
                    write_tickets()
                elif ticket['appointment'] == ticket_to_cancel and existing_tickets.count(ticket['appointment']) >= 2 and not deleted:
                    seat_to_write = input('There are more tickets for same appointment, enter wich seat you want to cancel: ')
                    for ticket1 in tickets_sold:
                        if ticket1['appointment'] == ticket_to_cancel and ticket1['seat'] == seat_to_write:
                            ticket1['status'] = 'canceled\n'
                            existing_tickets.remove(ticket['appointment'])
                            deleted = True
                            write_tickets()
                            break
            if deleted:
                break
            else:
                print('Entered seat not among tickets. Try again.')
        for app in seats_for_appointment:
            if app['code'] == ticket_to_cancel:
                col, row = seat_to_write[0], seat_to_write[1:]

                col_index = ord(col) - ord('a')
                row_index = int(row)

                for appointment in apointments:
                    if app['code'] == appointment['code']:
                        hall_name = appointment['hall']

                for hall in halls:
                    if hall['name'] == hall_name:
                        seats_per_row = hall['columns']

                position = col_index * int(seats_per_row) + row_index - 1

                seats = app['seats']
                list_of_seats = seats.split(',')

                list_of_seats[position] = seat_to_write

                joined_seats = ','.join(list_of_seats)

                app['seats'] = joined_seats

                write_seats_for_appointment()

        print('Succesefully canceled a ticket.')
        deleted = False
        cont = input('Continue canceling ot X to go back to menu: ')

        if cont.lower() == 'x':
            break


def direct_selling_tickets():
    existing_app_codes = []
    seats = None
    for code in apointments:
        if code['status'] == 'active\n':
            existing_app_codes.append(code['code'])
    while True:
        print('Currently avaliable appointments: ')
        movie_functions.print_table_projection(projections, apointments)

        print('Enter the code of appointment of movie projection you want to sell ticket for(x to go back) ')
        while True:
            ticket_code = input('Enter the code here: ')
            if ticket_code.lower() == 'x':
                break
            if ticket_code not in existing_app_codes:
                print(existing_app_codes)
                print('Entered code not in existing appointments. Try again')
            else:
                break
        if ticket_code.lower() == 'x':
            break
        for i in seats_for_appointment:
            if ticket_code in i['code']:
                seats = i['seats'].split(',')

        while True:
            name_surname = input('Enter name and surname for unregistered user or username for registered user: ')
            if not name_surname:
                print('Name or surname must include at least one character. Please try again.')
            else:
                break

        while True:
            print_seats(ticket_code)
            print(seats)
            chosen_seat = input('Choose one of best free seats for customer: ')
            if chosen_seat not in seats:
                print('You entered filled or not existing seat, please try again.')
            else:
                break
        for i, seat in enumerate(seats):
            if seat == chosen_seat:
                seats[i] = 'X'

        result_seats = ','.join(seats)
        for i in seats_for_appointment:
            if ticket_code in i['code']:
                i['seats'] = result_seats
        write_seats_for_appointment()

        new_ticket = {
            'name': name_surname,
            'appointment': ticket_code,
            'seat': chosen_seat,
            'date_sold': datetime.datetime.now().strftime('%d.%m.%Y'),
            'status': 'sold\n'
        }

        tickets_sold.append(new_ticket)
        write_tickets()
        cont = input('Succesefully sold a ticket, press enter to sell more or press x to go back to menu: ')
        if cont.lower() == 'x':
            break


def selling_reserved_tickets(user):
    existing_reserved_tickets = []
    sold = False
    for ticket in tickets_reserved:
        if ticket['status'] != 'canceled\n':
            existing_reserved_tickets.append(ticket['appointment'])
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%d.%m.%Y")

    while True:
        print('Currently reserved tickets: ')
        print_reserved_tickets_employee(tickets_reserved, tickets_sold)

        while True:
            ticket_code = input('Enter the code of ticket you want to sell here(x to back): ')
            if ticket_code.lower() == 'x':
                break
            if ticket_code not in existing_reserved_tickets:
                print('Entered code not in existing reserved tickets. Try again')
            else:
                break
        if ticket_code.lower() == 'x':
            break

        while not sold:
            for ticket in tickets_reserved:
                if ticket['appointment'] == ticket_code and existing_reserved_tickets.count(ticket['appointment']) < 2 and not sold:
                    ticket['status'] = 'sold\n'
                    ticket['date_sold'] = formatted_date
                    write_tickets()
                    sold = True
                elif ticket['appointment'] == ticket_code and existing_reserved_tickets.count(ticket['appointment']) >= 2 and not sold:
                    seat_to_sell = input('There are more tickets for same appointment, enter wich seat you want to sell: ')
                    for ticket1 in tickets_reserved:
                        if ticket1['appointment'] == ticket_code and ticket1['seat'] == seat_to_sell:
                            ticket1['status'] = 'sold\n'
                            ticket1['date_sold'] = formatted_date
                            existing_reserved_tickets.remove(ticket['appointment'])
                            write_tickets()
                            sold = True
                if sold:
                    break
                else:
                    print('Entered seat is not among reserved tickets. Try again.')

        sold = False
        cont = input('Succesefully sold a ticket, press enter to sell more or press x to go back to menu: ')
        if cont.lower() == 'x':
            break


def filter_tickets(choice):
    matching_tickets = []
    value = choice_keys[choice]
    filtered = False

    if choice in '1,2'.split(','):
        while True:
            data_input = input('Enter the appointment code for ticket you are searching(x to go back): ')
            if validations.is_empty_string(data_input):
                break
            elif data_input == 'x':
                break
            else:
                print('Empty string is not valid input. Try again')

    elif choice in '4,5'.split(','):
        while True:
            user_input = input(f'Write the {value} you are interested in(x to go back): ')
            if validations.is_valid_time_format(user_input):
                if choice == '4':
                    filter_starting_time(user_input)
                    filtered = True
                elif choice == '5':
                    filter_ending_time(user_input)
                    filtered = True
                break
            elif user_input.lower() == 'x':
                break
            else:
                print('Not a valid time format. Correct example: 20:00')
    elif choice == '3':
        while True:
            date_input = input(f'Write the date you are interested in(x to go back): ')
            if validations.is_valid_date_format(date_input):
                check_date_appointment(date_input)
                filtered = True
                break
            elif date_input.lower() == 'x':
                break
            else:
                print('Not a valid date format. Correct example: 12.12.2024')
    elif choice == '6':
        while True:
            data_input = input(f'Write the ticket status you are interested in(reserved/sold)(x to go back): ')
            if validations.reserved_sold(data_input):
                break
            elif data_input.lower() == 'x':
                break
            else:
                print('Not a valid ticket status. Possible input is reserved or sold.')
    if not filtered:
        matching_tickets_reserved = [ticket for ticket in tickets_reserved if ticket_filter_functions[value](data_input, ticket[value])]
        matching_tickets_sold = [ticket for ticket in tickets_sold if ticket_filter_functions[value](data_input, ticket[value])]
        if matching_tickets_reserved or matching_tickets_sold:
            print('Tickets that fit your willing: \n')
            print_reserved_tickets_employee(matching_tickets_reserved, matching_tickets_sold)
            input('Enter to continue...')
        else:
            input('Unfortunelly there is no ticket that fits your willing.')
            return
    filtered = False


def filter_code(user_input, app_code):
    return user_input == app_code


def filter_name(user_input, name):
    return user_input == name


def filter_status(user_input, status):
    return user_input in status


def check_date_appointment(user_input):
    tickets_r = []
    tickets_s = []

    for apointment in apointments:
        if user_input == apointment["date"].strip():
            for ticket in tickets_reserved:
                if ticket['appointment'] in apointment['code']:
                    tickets_r.append(ticket)
    for apointment in apointments:
        if user_input == apointment["date"].strip():
            for ticket in tickets_sold:
                if ticket['appointment'] in apointment['code']:
                    tickets_s.append(ticket)

            print_reserved_tickets_employee(tickets_r, tickets_s)
            input('Enter to continue...')
            return
    print('Unfortunaly there is no movie ticket for that date.')
    return


def filter_starting_time(user_input):
    tickets_r = []
    tickets_s = []

    for projection in projections:
        if user_input == projection['starting time']:
            for ticket in tickets_reserved:
                if projection['code'] in ticket['appointment']:
                    tickets_r.append(ticket)
    for projection in projections:
        if user_input == projection['starting time']:
            for ticket in tickets_sold:
                if projection['code'] in ticket['appointment']:
                    tickets_s.append(ticket)

            print_reserved_tickets_employee(tickets_r, tickets_s)
            input('Enter to continue...')
            return
    print('Unfortunaly there is no movie ticket for that starting time.')
    return


def filter_ending_time(user_input):
    tickets_r = []
    tickets_s = []

    for projection in projections:
        if user_input == projection['ending time']:
            for ticket in tickets_reserved:
                if projection['code'] in ticket['appointment']:
                    tickets_r.append(ticket)
    for projection in projections:
        if user_input == projection['ending time']:
            for ticket in tickets_sold:
                if projection['code'] in ticket['appointment']:
                    tickets_s.append(ticket)

            print_reserved_tickets_employee(tickets_r, tickets_s)
            input('Enter to continue...')
            return
    print('Unfortunaly there is no movie ticket for that starting time.')
    return


choice_keys = {
    '1': 'appointment',
    '2': 'name',
    '3': 'date_app',
    '4': 'starting time',
    '5': 'ending time',
    '6': 'status'

}

ticket_filter_functions = {
    'appointment': filter_code,
    'name': filter_name,
    'date_app': check_date_appointment,
    'starting time': filter_starting_time,
    'ending time': filter_ending_time,
    'status': filter_status
}


def search_for_ticket(user):
    while True:
        print_reserved_tickets_employee(tickets_reserved, tickets_sold)

        print('Enter categorie for searching: \n')
        print('1. Appointment code')
        print('2. Username/Name and surname')
        print('3. Date of appointment')
        print('4. Starting time')
        print('5. Ending time')
        print('6. Ticket status (reserved/sold)')
        print('7. Back to the main menu')

        choice = input('Enter your choice: ')

        if choice == '7':
            break
        elif choice in '1,2,3,4,5,6'.split(','):
            filter_tickets(choice)
        else:
            print('Not existing choice. Try again')


def change_ticket_data(ticket, changed, existing_tickets):
    while not changed:
        print('Enter the what do you want to change about a ticket: \n')
        print('1. Change the projection appointment')
        print('2. Change Name/Surname or username')
        print('3. Change the seat for ticket')
        print('4. Go back')
        choice = input('Enter your choice: ')

        if choice == '1':
            while True:
                new_appointment = input('Enter the code of new appointment: ')
                if new_appointment not in existing_tickets:
                    print('Entered code is not among existing ones. Try again')
                else:
                    break
            for i in seats_for_appointment:
                if new_appointment in i['code']:
                    seats = i['seats'].split(',')
            while True:
                chosen_seat = ticket['seat']
                if chosen_seat not in seats:
                    print('The seat for this ticket is unfotrunally filled in new appointment. Try again')
                    break
                else:
                    for app in seats_for_appointment:
                        if app['code'] == ticket['appointment']:
                            col, row = chosen_seat[0], chosen_seat[1:]

                            col_index = ord(col) - ord('a')
                            row_index = int(row)

                            for appointment in apointments:
                                if app['code'] == appointment['code']:
                                    hall_name = appointment['hall']

                            for hall in halls:
                                if hall['name'] == hall_name:
                                    seats_per_row = hall['columns']

                            position = col_index * int(seats_per_row) + row_index - 1

                            seats = app['seats']
                            list_of_seats = seats.split(',')
                            print(list_of_seats)
                            list_of_seats[position] = chosen_seat

                            joined_seats = ','.join(list_of_seats)
                            print(joined_seats)
                            app['seats'] = joined_seats

                            write_seats_for_appointment()
                    ticket['appointment'] = new_appointment
                    write_tickets()
                    for app in seats_for_appointment:
                        if app['code'] == new_appointment:
                            seats = app['seats']
                    splited_seats = seats.split(',')
                    for i, seat in enumerate(splited_seats):
                        if seat == chosen_seat:
                            splited_seats[i] = 'X'

                    result_seats = ','.join(splited_seats)
                    print(result_seats)
                    for i in seats_for_appointment:
                        if new_appointment in i['code']:
                            i['seats'] = result_seats
                    write_seats_for_appointment()

                changed = True
                input('Succesefully changed the ticket. Enter to continue...')
                break


def changing_tickets():
    changed = False
    existing_tickets = []
    existing_names = []
    existing_seats = []
    for reserved in tickets_reserved:
        existing_tickets.append(reserved['appointment'])
        existing_names.append(reserved['name'])
        existing_seats.append(reserved['seat'])

    for sold in tickets_sold:
        existing_tickets.append(sold['appointment'])
        existing_names.append(sold['name'])
        existing_seats.append(sold['seat'])

    for app in apointments:
        existing_tickets.append(app['code'])
    while True:
        print(existing_tickets)
        print('These are tickets that you can cancel:')
        print_reserved_tickets_employee(tickets_reserved, tickets_sold)
        deleted = False
        while True:
            ticket_to_change = input('Enter the appointment code for reservation you want to change the data for(x to go back): ')

            if ticket_to_change.lower() == 'x':
                break
            if ticket_to_change not in existing_tickets:
                print('There is no reservation with that code, please try again.')
            else:
                break
        if ticket_to_change.lower() == 'x':
            break

        while True:
            name = input('Enter the Name/surname or username for ticket you want to change the data for(x to go back): ')

            if name.lower() == 'x':
                break
            if name not in existing_names:
                print('There is no ticket with that Name/Surname or username, please try again.')
            else:
                break
        if name.lower() == 'x':
            break

        while True:
            seat = input('Enter the seat for ticket you want to change the data for(x to go back): ')

            if seat.lower() == 'x':
                break
            if seat not in existing_seats:
                print('There is no ticket with that seat, please try again.')
            else:
                break
        if seat.lower() == 'x':
            break

        while True:
            for ticket in tickets_reserved:
                if ticket['appointment'] == ticket_to_change and ticket['name'] == name and ticket['seat'] == seat:
                    change_ticket_data(ticket, changed, existing_tickets)
            if changed:
                break
            for ticket in tickets_sold:
                if ticket['appointment'] == ticket_to_change and ticket['name'] == name and ticket['seat'] == seat:
                    change_ticket_data(ticket, changed, existing_tickets)
            if changed:
                break
            else:
                print('Entered data not among tickets. Try again.')
                break
