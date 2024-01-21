import movie_functions
from movie_functions import projections
from movie_functions import apointments
import datetime
import tabulate

tickets_reserved = []
tickets_sold = []
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


def print_reserved_tickets_employee(user):
    headers = ["#", "Appointment code","Username/Name and surname", "Movie name", "Date of appointment", "Starting time", "Ending time", "Seat", "Ticket status"]
    table_data = []
    num = 1
    for ticket_r in tickets_reserved:
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

                table_data.append(table_row)
                num += 1
    for ticket_s in tickets_sold:
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
        print(seats_for_appointment)
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
        print_reserved_tickets_employee(user)
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
        for ticket in tickets_reserved:
            if ticket['name'] == user['username'] and ticket['appointment'] == ticket_to_cancel and existing_tickets.count(ticket['appointment']) < 2 and not deleted:
                ticket['status'] = 'canceled\n'
                seat_to_write = ticket['seat']
                write_tickets()
            elif ticket['name'] == user['username'] and ticket['appointment'] == ticket_to_cancel and existing_tickets.count(ticket['appointment']) >= 2 and not deleted:
                seat_to_write = input('There are more tickets for same appointment, enter wich seat you want to cancel: ')
                for ticket1 in tickets_reserved:
                    if ticket1['appointment'] == ticket_to_cancel and ticket1['seat'] == seat_to_write:
                        ticket1['status'] = 'canceled\n'
                        existing_tickets.remove(ticket['appointment'])
                        deleted = True
                        write_tickets()
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
