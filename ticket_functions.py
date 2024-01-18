import movie_functions
from movie_functions import projections
from movie_functions import apointments
import datetime

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


def print_seats(movie_code):
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
    existing_app_codes = []
    for code in seats_for_appointment:
        existing_app_codes.append(code['code'])
    if not user:
        while True:
            name_surname = input('You are not registered, please enter name and surname for your ticket reservation: ')
            if not name_surname:
                print('Name or surname must include at least one character. Please try again.')
            else:
                break

    while True:
        print(seats_for_appointment)
        movie_functions.print_table_projection(projections, apointments)
        print('Enter the code of appointment of movie projection you want to buy ticket for ')
        while True:
            ticket_code = input('Enter the code here: ')
            if ticket_code not in existing_app_codes:
                print(existing_app_codes)
                print('Entered code not in existing appointments. Try again')
            else:
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

        if user:
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
        break
