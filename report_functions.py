import tabulate
from movie_functions import projections
from movie_functions import apointments
from ticket_functions import sold_ticket_info
from ticket_functions import appointment_info
from ticket_functions import users
from ticket_functions import tickets_sold
from datetime import datetime, timedelta
import validations


def find_projection_code(movie_name, projection):
    if projection['movie name'].lower() == movie_name.lower():
        return projection['code']


def is_date_in_last_30_days(date_str):
    date_object = datetime.strptime(date_str, "%d.%m.%Y")
    difference = datetime.now() - date_object
    return difference <= timedelta(days=30)


def print_table_reports(table_data, headers):
    table = tabulate.tabulate(table_data, headers=headers, tablefmt='grid')
    print(table)


def save_report(data_list):
    with open('reports.txt', 'a') as fin:
        line = '|'.join(value.replace('\n', '') for data in data_list for value in data.values())
        fin.write(line + '\n')


def report_num1():
    table_data = []
    data_to_save = []
    headers = ['#', 'Username or Name/Surname', 'Appointment code', 'Seat', 'Date sold', 'Status']
    while True:
        while True:
            date_input = input('Enter the selling date you want to get report for(x to go back): ')
            if validations.is_valid_date_format(date_input):
                num = 1
                for ticket in tickets_sold:
                    if ticket['date_sold'] == date_input:
                        data_to_save.append(ticket)
                        table_row = [
                            num,
                            ticket['name'],
                            ticket['appointment'],
                            ticket['seat'],
                            ticket['date_sold'],
                            ticket['status']
                        ]
                        table_data.append(table_row)
                        num += 1
                break
            elif date_input.lower() == 'x':
                break
            else:
                print('Not a valid date format. Correct example: 12.12.2024')
        if date_input.lower() == 'x':
            break
        print_table_reports(table_data, headers)
        while True:
            choice_to_save = input('Do you want to save this report(yes/no): ')
            if choice_to_save == 'yes':
                save_report(data_to_save)
                input('Succesefully saved the report. Enter to go back...')
                break
            elif choice_to_save == 'no':
                break
            else:
                print('Not existing choice.')
        break


def report_num2():
    table_data = []
    data_to_save = []
    tickets_added = []
    headers = ['#', 'Username or Name/Surname', 'Appointment code', 'Seat', 'Date sold', 'Status']
    while True:
        while True:
            date_input = input('Enter the date of appointment you want to get report for(x to go back): ')
            if validations.is_valid_date_format(date_input):
                num = 1
                for ticket1 in sold_ticket_info:
                    if ticket1['date_of_appointment'] == date_input:
                        for ticket in tickets_sold:
                            if ticket1['appointment'] == ticket['appointment'] and ticket not in tickets_added:
                                tickets_added.append(ticket)
                                data_to_save.append(ticket)
                                table_row = [
                                    num,
                                    ticket['name'],
                                    ticket['appointment'],
                                    ticket['seat'],
                                    ticket['date_sold'],
                                    ticket['status']
                                ]
                                table_data.append(table_row)
                                num += 1
                break
            elif date_input.lower() == 'x':
                break
            else:
                print('Not a valid date format. Correct example: 12.12.2024')
        if date_input.lower() == 'x':
            break
        print_table_reports(table_data, headers)
        while True:
            choice_to_save = input('Do you want to save this report(yes/no): ')
            if choice_to_save == 'yes':
                save_report(data_to_save)
                input('Succesefully saved the report. Enter to go back...')
                break
            elif choice_to_save == 'no':
                break
            else:
                print('Not existing choice.')
        break


def report_num3():
    table_data = []
    data_to_save = []
    tickets_added = []
    employees = []
    for user in users:
        if user['role'] == 'employee\n':
            employees.append(user['username'])
    headers = ['#', 'Employee', 'Username or Name/Surname', 'Appointment code', 'Seat', 'Date sold', 'Status']
    while True:
        while True:
            print(employees)
            employee = input('Enter the employee you want to get report for(x to go back): ')

            if employee not in employees:
                print('Entered employee username not in existing employees.')
            elif employee.lower() == 'x':
                break
            else:
                break
        if employee.lower() == 'x':
            break
        while True:
            date_input = input('Enter the date of appointment you want to get report for(x to go back): ')
            if validations.is_valid_date_format(date_input):
                num = 1
                for ticket1 in sold_ticket_info:
                    if ticket1['date_of_appointment'] == date_input and ticket1['employee'] == employee:
                        for ticket in tickets_sold:
                            if ticket1['appointment'] == ticket['appointment'] and ticket not in tickets_added:
                                tickets_added.append(ticket)
                                data_to_save.append(ticket)
                                table_row = [
                                    num,
                                    employee,
                                    ticket['name'],
                                    ticket['appointment'],
                                    ticket['seat'],
                                    ticket['date_sold'],
                                    ticket['status']
                                ]
                                table_data.append(table_row)
                                num += 1
                break
            elif date_input.lower() == 'x':
                break
            else:
                print('Not a valid date format. Correct example: 12.12.2024')
        if date_input.lower() == 'x':
            break
        print_table_reports(table_data, headers)
        while True:
            choice_to_save = input('Do you want to save this report(yes/no): ')
            if choice_to_save == 'yes':
                save_report(data_to_save)
                input('Succesefully saved the report. Enter to go back...')
                break
            elif choice_to_save == 'no':
                break
            else:
                print('Not existing choice.')
        break


def report_num4():
    table_data = []
    data_to_save = []
    headers = ['Number of sold tickets', 'Total price of sold tickets']
    while True:
        while True:
            day_input = input('Enter the selling day in week you want to get report for(x to go back): ')

            if day_input.lower() == 'x':
                break
            elif not validations.is_valid_day_of_week(day_input):
                print('Entered day is not either monday, tuesday, wednesday, thursday, friday, saturday or sunday.')
            else:
                break
        if day_input.lower() == 'x':
            break

        total_number = 0
        total_price = 0.0

        for ticket1 in sold_ticket_info:
            date_object = datetime.strptime(ticket1['date_sold'], "%d.%m.%Y")
            day_of_week = date_object.strftime("%A").lower()
            if day_input == day_of_week:
                for ticket in tickets_sold:
                    if ticket['seat'] == ticket1['seat'] and ticket['appointment'] == ticket1['appointment']:
                        total_number += 1
                        total_price += float(ticket1['price'])

        table_data.append([str(total_number), str(total_price)])
        data_to_save.append({
            'day': day_input,
            'total_number': str(total_number),
            'total_price': str(total_price)
        })

        print_table_reports(table_data, headers)
        while True:
            choice_to_save = input('Do you want to save this report(yes/no): ')
            if choice_to_save == 'yes':
                save_report(data_to_save)
                input('Succesefully saved the report. Enter to go back...')
                break
            elif choice_to_save == 'no':
                break
            else:
                print('Not existing choice.')
        break


def report_num5():
    table_data = []
    data_to_save = []
    headers = ['Number of sold tickets', 'Total price of sold tickets']
    while True:
        while True:
            day_input = input('Enter the projection day in week you want to get report for(x to go back): ')

            if day_input.lower() == 'x':
                break
            elif not validations.is_valid_day_of_week(day_input):
                print('Entered day is not either monday, tuesday, wednesday, thursday, friday, saturday or sunday.')
            else:
                break
        if day_input.lower() == 'x':
            break

        total_number = 0
        total_price = 0.0

        for ticket1 in sold_ticket_info:
            date_object = datetime.strptime(ticket1['date_of_appointment'], "%d.%m.%Y")
            day_of_week = date_object.strftime("%A").lower()
            if day_input == day_of_week:
                for ticket in tickets_sold:
                    if ticket['seat'] == ticket1['seat'] and ticket['appointment'] == ticket1['appointment']:
                        total_number += 1
                        total_price += float(ticket1['price'])

        table_data.append([str(total_number), str(total_price)])
        data_to_save.append({
            'day': day_input,
            'total_number': str(total_number),
            'total_price': str(total_price)
        })

        print_table_reports(table_data, headers)
        while True:
            choice_to_save = input('Do you want to save this report(yes/no): ')
            if choice_to_save == 'yes':
                save_report(data_to_save)
                input('Succesefully saved the report. Enter to go back...')
                break
            elif choice_to_save == 'no':
                break
            else:
                print('Not existing choice.')
        break


def report_num6():
    table_data = []
    data_to_save = []
    movies_existing = []
    for movie in projections:
        movies_existing.append(movie['movie name'].lower())
    headers = ['Number of sold tickets', 'Total price of sold tickets']
    while True:
        while True:
            print(movies_existing)
            movie_input = input('Enter the projection day in week you want to get report for(x to go back): ')

            if movie_input.lower() == 'x':
                break
            elif movie_input.lower() not in movies_existing:
                print('This movie is not among existing ones.')
            else:
                break
        if movie_input.lower() == 'x':
            break

        total_number = 0
        total_price = 0.0
        projection_codes = []
        for proj in projections:
            if movie_input.lower() == proj['movie name'].lower():
                projection_codes.append(find_projection_code(movie_input, proj))
        print(projection_codes)
        for ticket1 in sold_ticket_info:
            if ticket1['appointment'][:4] in projection_codes:
                for ticket in tickets_sold:
                    if ticket['seat'] == ticket1['seat'] and ticket['appointment'] == ticket1['appointment']:
                        total_number += 1
                        total_price += float(ticket1['price'])

        table_data.append([str(total_number), str(total_price)])
        data_to_save.append({
            'movie': movie_input,
            'total_number': str(total_number),
            'total_price': str(total_price)
        })

        print_table_reports(table_data, headers)
        while True:
            choice_to_save = input('Do you want to save this report(yes/no): ')
            if choice_to_save == 'yes':
                save_report(data_to_save)
                input('Succesefully saved the report. Enter to go back...')
                break
            elif choice_to_save == 'no':
                break
            else:
                print('Not existing choice.')
        break


def report_num7():
    table_data = []
    data_to_save = []
    employees = []
    for user in users:
        if user['role'] == 'employee\n':
            employees.append(user['username'])
    headers = ['Number of sold tickets', 'Total price of sold tickets']
    while True:
        while True:
            print(employees)
            employee = input('Enter the employee you want to get report for(x to go back): ')

            if employee not in employees:
                print('Entered employee username not in existing employees.')
            elif employee.lower() == 'x':
                break
            else:
                break
        if employee.lower() == 'x':
            break
        while True:
            date_input = input('Enter the date of appointment you want to get report for(x to go back): ')
            if validations.is_valid_date_format(date_input):
                break
            elif date_input.lower() == 'x':
                break
            else:
                print('Not a valid date format. Correct example: 12.12.2024')
        if date_input.lower() == 'x':
            break

        total_number = 0
        total_price = 0.0

        for ticket1 in sold_ticket_info:
            if ticket1['date_sold'] == date_input and ticket1['employee'] == employee:
                for ticket in tickets_sold:
                    if ticket['seat'] == ticket1['seat'] and ticket['appointment'] == ticket1['appointment']:
                        total_number += 1
                        total_price += float(ticket1['price'])

        table_data.append([str(total_number), str(total_price)])
        data_to_save.append({
            'date_sold': date_input,
            'employee': employee,
            'total_number': str(total_number),
            'total_price': str(total_price)
        })

        print_table_reports(table_data, headers)
        while True:
            choice_to_save = input('Do you want to save this report(yes/no): ')
            if choice_to_save == 'yes':
                save_report(data_to_save)
                input('Succesefully saved the report. Enter to go back...')
                break
            elif choice_to_save == 'no':
                break
            else:
                print('Not existing choice.')
        break


def report_num8():
    table_data = []
    data_to_save = []
    employees = []
    for user in users:
        if user['role'] == 'employee\n':
            employees.append(user['username'])
    headers = ['Employee', 'Number of sold tickets', 'Total price of sold tickets']

    for employee in employees:
        total_number = 0
        total_price = 0.0
        for ticket1 in sold_ticket_info:
            if ticket1['employee'] == employee:
                for ticket in tickets_sold:
                    if ticket['seat'] == ticket1['seat'] and ticket['appointment'] == ticket1['appointment'] and is_date_in_last_30_days(ticket1['date_sold']):
                        total_number += 1
                        total_price += float(ticket1['price'])
        table_row = [
            employee,
            str(total_number),
            str(total_price),
        ]
        table_data.append(table_row)

        data_to_save.append({
            'employee': employee,
            'total_number': str(total_number),
            'total_price': str(total_price)
        })

    print_table_reports(table_data, headers)
    while True:
        choice_to_save = input('Do you want to save this report(yes/no): ')
        if choice_to_save == 'yes':
            save_report(data_to_save)
            input('Succesefully saved the report. Enter to go back...')
            break
        elif choice_to_save == 'no':
            break
        else:
            print('Not existing choice.')


def manager_reports():
    while True:
        print('These are reports you can get: ')
        print('1. List of sold tickets for one date of selling')
        print('2. List of sold tickets for one date of appointment')
        print('3. List of sold tickets for one selling date and one employee')
        print('4. Total number and price of sold tickets for one day in week(selling day)')
        print('5. Total number and price of sold tickets for one day in week(projection day)')
        print('6. Total price of sold tickets for one movie')
        print('7. Total number and price of sold tickets for selling day and one employee')
        print('8. Total number and price of sold tickets for each employee(last 30 days)')
        print('9. Back to the menu')

        choice = input('Enter tour choice: ')

        if choice == '1':
            report_num1()
            break
        elif choice == '2':
            report_num2()
            break
        elif choice == '3':
            report_num3()
            break
        elif choice == '4':
            report_num4()
            break
        elif choice == '5':
            report_num5()
            break
        elif choice == '6':
            report_num6()
            break
        elif choice == '7':
            report_num7()
            break
        elif choice == '8':
            report_num8()
            break
        elif choice == '9':
            break
        else:
            print('Not existing choice.')