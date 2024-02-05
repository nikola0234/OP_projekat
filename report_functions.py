import tabulate
from movie_functions import projections
from movie_functions import apointments
from ticket_functions import sold_ticket_info
from ticket_functions import appointment_info
from ticket_functions import tickets_sold
import validations


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



