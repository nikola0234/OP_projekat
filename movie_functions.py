# U ovom fajlu se nalaze funcije koje omogucavaju korisnicima pretrage filmova.
import os
from datetime import datetime, timedelta
from tabulate import tabulate
import re


def clear_screen1():
    os.system('cls' if os.name == 'nt' else 'clear')


movies = []
apointments = []
projections = []
cinema_halls = []


def is_valid_time_format(input_str):
    time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    return bool(re.match(time_pattern, input_str))


def is_valid_date_format(input_str):
        try:
            datetime_object = datetime.strptime(input_str, '%d.%m.%Y')
            return True
        except ValueError:
            return False


def generate_appointments_from_projections():
    with open('projections.txt', 'r') as fin:
        projections = fin.readlines()

    current_date = datetime.now().date()
    existing_dates = []
    existing_codes = []
    existing_codes_app = []

    with open('projection_appointment.txt', 'r') as fin:
        for data in fin:
            app_data = data.strip().split('|')

            if len(app_data) == 4 and app_data[3] == 'active':
                existing_dates.append(app_data[1])
                existing_codes_app.append(app_data[0])

    for proj in projections:
        proj_data = proj.strip().split('|')
        for code in existing_codes_app:
            if proj_data[0] in code:
                existing_codes.append(proj_data[0])

    appointments = []
    for projection in projections:
        projection_data = projection.strip().split('|')

        code = projection_data[0]
        days = projection_data[4].split(', ')
        hall = projection_data[1]

        if 'deleted' in projection_data:
            continue
        for i in range(14):
            appointment_date = current_date + timedelta(days=i)

            if appointment_date.strftime('%A').lower() in [day.lower() for day in days]:
                letter1 = chr((i // 26) % 26 + ord('A'))
                letter2 = chr((i % 26) + ord('A'))
                appointment_code = f"{code}{letter1}{letter2}"
                appointment_format = f"{appointment_code}|{appointment_date.strftime('%d.%m.%Y')}|{hall}|{'active'}"

                if (appointment_date.strftime('%d.%m.%Y') not in existing_dates) or (code not in existing_codes):
                    appointments.append(appointment_format)
                    existing_dates.append(appointment_date.strftime('%d.%m.%Y'))

    with open('projection_appointment.txt', 'a') as fin:
        for appointment in appointments:
            fin.write(appointment + '\n')


def print_movies_table(movies):
    headers = ["#", "Name", "Genre", "Duration(min)", "Film director", "Main roles", "Country of production", "Year of creation", "Summary"]
    table_data = []

    for number, movie in enumerate(movies, start=1):
        table_row = [
            number,
            movie['name'],
            movie['genre'],
            movie['duration'],
            movie['film director'],
            movie['actors'],
            movie['country of production'],
            movie['year of production'],
            movie['summary']
        ]
        if movie['status'] == 'active\n':
            table_data.append(table_row)

    table = tabulate(table_data, headers=headers, tablefmt='grid')
    print(table)


def read_movies():
    with open('movies.txt', 'r') as fin:
        for line in fin:
            movie = line.split('|')
            movies.append({
                'name': movie[0],
                'genre': movie[1],
                'duration': movie[2],
                'film director': movie[3],
                'actors': movie[4],
                'country of production': movie[5],
                'year of production': movie[6],
                'summary': movie[7],
                'status': movie[8]
            })


def write_movies():
    with open('movies.txt', 'w') as fin:
        for movie in movies:
            fin.write(movie['name'] + '|' +
                      movie['genre'] + '|' +
                      movie['duration'] + '|' +
                      movie['film director'] + '|' +
                      movie['actors'] + '|' +
                      movie['country of production'] + '|' +
                      movie['year of production'] + '|' +
                      movie['summary'] + '|' +
                      movie['status'])


def update_movie_list():
    movies.clear()
    read_movies()


def read_cinema_hall():
    with open('cienma_halls.txt', 'r') as fin:
        for line in fin:
            hall = line.split('|')
            cinema_halls.append(hall[0])


def avaliable_movies():
    clear_screen1()
    print('\n The movies we are currently showing: \n')
    print_movies_table(movies)
    input('Enter to go back...')
    clear_screen1()


def add_new_movie():
    clear_screen1()
    while True:
        print("Enter the data for movie you are adding: \n")
        name = input('Enter the name of movie(x to go back): ')
        if name == 'x':
            break
        genre = input('Enter the genre of movie: ')
        while True:
            duration = input('Enter the duration of movie(in minutes): ')
            if duration.isdigit():
                break
            else:
                print('Duration needs to be in format: 120')
        director = input('Enter the film director: ')
        main_roles = input('Enter the main actors: ')
        country = input('Enter the country of production: ')
        year = input('Enter the year of creation: ')
        summary = input('Enter the short summary of movie: ')

        if not all([name, genre, duration, director, main_roles, country, year, summary]):
            print("Please fill in all the data. None of the data can be empty. Try again.\n")
            continue
        with open('movies.txt', 'a') as fin:
            fin.write(name + '|' + genre + '|' + duration + '|' + director + '|' + main_roles + '|' + country + '|'
                      + year + '|' + summary + '|' + 'active\n')
        movies.clear()
        read_movies()
        print('\nNew movie successfully added!')
        input('Enter to continue...')
        break


def delete_movie():
    clear_screen1()
    while True:
        print('Currently avaliable movies: \n')
        print_movies_table(movies)
        name = input('Enter the name of movie you want to delete(x to go back): ')
        if name.lower() == 'x':
            movies.clear()
            read_movies()
            delete_appointmets_after_projection()
            break
        for movie in movies:
            if movie['name'].lower() == name.lower():
                movie['status'] = 'deleted\n'
                write_movies()
                delete_projection_after_movie(name)
                input('Movie succesefully deleted, this action will be loaded after you go back to your menu! Enter to go back...')
                break
        else:
            input('The input is inapropriate, click enter and try again!')
            continue


def change_movie_data():
    clear_screen1()
    while True:
        print('Currently avaliable movies: \n')
        print_movies_table(movies)
        name = input('For which movie you want to change the data(x to go back): ')
        if name.lower() == 'x':
            break
        for movie in movies:
            if movie['name'].lower() == name.lower():
                categorie = input(
                    'What do you want to change about this movie(name, genre, director, actors, country,'
                    'year or summary)(enter one categorie): ')
                if categorie == 'name':
                    new_name = input('Enter the changed name of this movie: ')
                    movie['name'] = new_name
                    write_movies()
                    break
                elif categorie == 'genre':
                    new_genre = input('Enter the changed gender(s) of this movie: ')
                    movie['genre'] = new_genre
                    write_movies()
                    break
                elif categorie == 'director':
                    new_director = input('Enter the changed film director of this movie: ')
                    movie['director'] = new_director
                    write_movies()
                    break
                elif categorie == 'actors':
                    new_actor = input('Enter the changed actor(s) that played in this movie: ')
                    movie['actors'] = new_actor
                    write_movies()
                    break
                elif categorie == 'country':
                    new_country = input('Enter the changed country of production of this movie: ')
                    movie['country of production'] = new_country
                    write_movies()
                    break
                elif categorie == 'year':
                    new_year = input('Enter the changed year of production of this movie: ')
                    movie['year of production'] = new_year
                    write_movies()
                    break
                elif categorie == 'summary':
                    new_summary = input('Enter the changed summary of this movie: ')
                    movie['summary'] = new_summary
                    write_movies()
                    break
        else:
            input('The input is inapropriate, click enter and try again!')
            continue


def add_new_projection():
    print('Currently available movies are: \n')
    print_movies_table(movies)
    while True:
        movie_name = input('Enter the name of one of available movies to add the projection(x to go back): ')
        if movie_name.lower() == 'x':
            break
        all_names = []
        for movie in movies:
            all_names.append(movie['name'])

        if movie_name not in all_names:
            print('Your input does not match any movie, please try again.')
            continue

        while True:
            code = input('Enter the 4-digit projection code: ')
            if len(code) == 4:
                break
            else:
                 print('Code must include 4 digits!')

        while True:
            hall = input('Enter the new cinema hall for this projection: ')
            if hall in cinema_halls:
                break
            else:
                print('The entered hall is not available! The available ones are:')
                print(cinema_halls)

        while True:
            starting_time = input('Enter the starting time (format HH:MM): ')
            if is_valid_time_format(starting_time):
                break
            else:
                print('Not a valid time format. Correct example: 20:00')

            # Loop for ending time input with validation

        while True:
            ending_time = input('Enter the ending time (format HH:MM): ')
            if is_valid_time_format(ending_time):
                break
            else:
                print('Not a valid time format. Correct example: 20:00')

        days = input('Enter the days of projection: ')

        movie_name = input('Enter the movie name: ')

        price = input('Enter the starting price: ')

        days_list = days.split(',')

        if not all([code, hall, starting_time, ending_time, days, movie_name, price]):
            print("Please fill in all the data. None of the data can be empty. Try again.\n")
            continue

        with open('projections.txt', 'a') as fin:
            fin.write(code + '|' + hall + '|' + starting_time + '|' + ending_time + '|' + days + '|' +
                      movie_name + '|' + price + '|' + 'active' + '\n')
        print('\nNew projection successfully added!')
        generate_appointments_from_projections()
        input('Enter to continue...')
        break


def delete_movie_projection():
    clear_screen1()
    while True:
        print('Currently active movie projections: \n')
        print_table_projection(projections, apointments)
        projection = input('Enter the code of projection you want to delete(x to go back): ')

        if projection.lower() == 'x':
            write_projections()
            projections.clear()
            read_projections()
            delete_appointmets_after_projection()
            break
        for proj in projections:
            if projection == proj['code']:
                proj['status'] = 'deleted\n'
                input('Projection succesefully deleted, action will be loaded after you go back to your menu!Enter to go back...')
                break
        else:
                input('The input is inapropriate, click enter and try again!')
                continue


def delete_projection_after_movie(movie_name):
    for proj in projections:
        if proj['movie name'].lower() == movie_name.lower():
            proj['status'] = 'deleted\n'
            write_projections()


def delete_appointmets_after_projection():
    proj_codes = []
    for proj in projections:
        if proj['status'] == 'deleted\n':
            proj_codes.append(proj['code'])
    for proj in proj_codes:
        for app in apointments:
            if proj in app['code']:
                app['status'] = 'deleted\n'
    write_appointments()


def change_projection_data():
    clear_screen1()
    while True:
        print('Currently active movie projections: \n')
        print_table_projection(projections, apointments)
        code = input('Enter the code of projection you want to change(x to go back): ')

        if code.lower() == 'x':
            break

        projection_found = False

        for projection in projections:
            if projection['code'] == code:
                categorie = input('What do you want to change about projection(cinema hall, starting time,'
                                  ' ending time, days, starting price): ')
                if categorie.lower() == 'cinema hall':
                    while True:
                        new_hall = input('Enter the new cinema hall for this projection: ')
                        if new_hall in cinema_halls:
                            projection['cinema hall'] = new_hall
                            write_projections()
                            projection_found = True
                            break
                        else:
                            print('The entered hall is not available! The available ones are:')
                            print(cinema_halls)
                elif categorie.lower() == 'starting time':
                    while True:
                        new_starting_time = input('Enter the new starting time for this projection(format HH:MM): ')
                        if is_valid_time_format(new_starting_time):
                            projection['starting time'] = new_starting_time
                            write_projections()
                            projection_found = True
                            break
                        else:
                            print('Not a valid time format. Correct example: 20:00')
                elif categorie.lower() == 'ending time':
                    while True:
                        new_ending_time = input('Enter the new ending time for this projection(format HH:MM): ')
                        if is_valid_time_format(new_ending_time):
                            projection['ending time'] = new_ending_time
                            projection_found = True
                            break
                        else:
                            print('Not a valid time format. Correct example: 20:00')
                elif categorie.lower() == 'starting price':
                    new_price = input('Enter new starting price for this projection: ')
                    projection['price'] = new_price
                    write_projections()
                    projection_found = True
        if not projection_found:
            input('No projection fits entered code! Click enter and try again...')
            continue

# U narednom delu se nalaze funcije vezane za pretragu filmova.


def search_by_categories(categories):
    matching_movies = movies.copy()

    for category in categories:
        if category.lower() == 'duration':
            matching_movies = search_by_duration(matching_movies)
        else:
            user_input = input(f'Enter the {category} of movie you are willing to search for: ')
            matching_movies = [movie for movie in matching_movies if category_filter_functions[category](user_input, movie[category])]

    if matching_movies:
        print('Movies that fit your willing: \n')
        print_movies_table(matching_movies)
        input('Enter to go back...')
    else:
        input(f'\nNo movie fits your current willing, enter back and find the right one for you!')


def filter_name(user_input, movie_name):
    return user_input.lower() == movie_name.lower()


def filter_genre(user_input, movie_genre):
    movie_genre = [movie.strip() for movie in movie_genre.lower().split(',')]
    return user_input.lower() in movie_genre


def search_by_duration(movies):
    print('Would you like to filter movies for: \n')
    print('1. Max duration')
    print('2. Min duration')
    print('3. Range of duration')
    choice = input('Enter your choice: ')
    if choice == '1':
        maximum = eval(input('Enter the maximum duration of movie: '))
        return [movie for movie in movies if maximum >= eval(movie['duration'])]
    if choice == '2':
        minimum = eval(input('Enter the minimum duration of movie: '))
        return [movie for movie in movies if minimum <= eval(movie['duration'])]
    if choice == '3':
        minimum = eval(input('Enter the minimum duration of movie: '))
        maximum = eval(input('Enter the maximum duration of movie: '))
        return [movie for movie in movies if minimum <= eval(movie['duration']) <= maximum]
    else:
        print('Invalid choice. Returning back to original list.')


def filter_film_director(user_input, movie_film_director):
    return user_input.lower() == movie_film_director.lower()


def filter_actors(user_input, movie_actors):
    movie_actors = [actor.strip() for actor in movie_actors.lower().split(',')]
    return user_input in movie_actors


def filter_country(user_input, movie_country):
    return user_input.lower() == movie_country.lower()


def filter_year(user_input, movie_year):
    return user_input.lower() == movie_year.lower()


category_filter_functions = {
    'name': filter_name,
    'genre': filter_genre,
    'duration': search_by_duration,
    'film director': filter_film_director,
    'actors': filter_actors,
    'country of production': filter_country,
    'year of production': filter_year
}


def search_movie():
    while True:
        clear_screen1()
        print_movies_table(movies)
        print('Enter categorie for searching: \n')
        print('1. Name')
        print('2. Genre')
        print('3. Duration')
        print('4. Film Director')
        print('5. Actors')
        print('6. Country of production')
        print('7. Year of production')
        print('8. Back to main manu')

        categories_input = input('Enter the categories you want to search movies for (comma-separated and use words): ')
        if '8' == categories_input:
            clear_screen1()
            break

        selected_categories = [category.strip() for category in categories_input.split(',')]

        invalid_categories = [category for category in selected_categories if category not in category_filter_functions]
        if invalid_categories:
            print(f'Invalid categories: {", ".join(invalid_categories)}. Please enter valid options.')
            continue
        search_by_categories(selected_categories)


# U narednom delu se nalaze funcije vezane za pretragu termina bioskopskih projekcija


def read_appointment():
    with open('projection_appointment.txt', 'r') as fin:
        for projection in fin:
            ap = projection.split('|')
            apointments.append({
                'code': ap[0],
                'date': ap[1],
                'hall': ap[2],
                'status': ap[3]
            })


def write_appointments():
    with open('projection_appointment.txt', 'w') as fin:
        for ap in apointments:
            fin.write(
                ap['code'] + '|' +
                ap['date'] + '|' +
                ap['hall'] + '|' +
                ap['status']
            )


def read_projections():
    with open('projections.txt', 'r') as fin:
        for projection in fin:
            proj = projection.split('|')
            projections.append({
                'code': proj[0],
                'cinema hall': proj[1],
                'starting time': proj[2],
                'ending time': proj[3],
                'days': proj[4],
                'movie name': proj[5],
                'price': proj[6],
                'status': proj[7]
            })


def write_projections():
    with open('projections.txt', 'w') as fin:
        for proj in projections:
            fin.write(
                proj['code'] + '|' +
                proj['cinema hall'] + '|' +
                proj['starting time'] + '|' +
                proj['ending time'] + '|' +
                proj['days'] + '|' +
                proj['movie name'] + '|' +
                proj['price'] + '|' +
                proj['status']
            )


def print_table_projection(projection, appointment):
    headers = ["#", "Projection code", "Movie name", "Cinema hall", "Date of this projection", "Starting time", "Ending time", "Price"]
    table_data = []
    number = 1
    for appoint in appointment:
        for proj in projection:
            if proj['code'] in appoint['code']:
                table_row = [
                    number,
                    appoint["code"],
                    proj["movie name"],
                    proj["cinema hall"],
                    appoint["date"],
                    proj["starting time"],
                    proj["ending time"],
                    proj["price"]
                ]
                if proj['status'] == 'active\n':
                    table_data.append(table_row)
                    number += 1
    table = tabulate(table_data, headers=headers, tablefmt="grid")
    print(table)


def filter_projection(choice):
    matching_projection = projections.copy()
    matching_appointment = []

    if choice == '3':
        clear_screen1()
        while True:
            date_input = input(f'Write the date you are interested in: ')
            if is_valid_date_format(date_input):
                check_date_apointment(date_input)
                break
            else:
                print('Not a valid date format. Correct example: 12.12.2024')
        return
    elif choice in '12456':
        value = choice_keys[choice]
        if choice == '4':
            while True:
                user_input = input(f'Write the {value} you are interested in: ')
                if is_valid_time_format(user_input):
                    break
                else:
                    print('Not a valid time format. Correct example: 20:00')

        if choice == '5':
            while True:
                user_input = input(f'Write the {value} you are interested in: ')
                if is_valid_time_format(user_input):
                    break
                else:
                    print('Not a valid time format. Correct example: 20:00')
        elif choice == '2':
            while True:
                user_input = input(f'Write the {value} you are interested in: ')
                if user_input in cinema_halls:
                    break
                else:
                    print('The entered hall is not available! The available ones are:')
                    print(cinema_halls)
        elif choice in '16':
            user_input = input(f'Write the {value} you are interested in: ')
        matching_projection = [projection for projection in projections if projection_filter_functions[value](user_input, projection[value])]
    if matching_projection:
        print('Movie projections that fit your willing: \n')
        for projection in matching_projection:
            for apointment in apointments:
                if projection['code'] in apointment['code']:
                    matching_appointment.append(apointment)
        print_table_projection(matching_projection, matching_appointment)
        input('Enter to continue...')
    else:
        clear_screen1()
        print('Unfortunally there is no movie projection that fit your willing.')
        return


def check_date_apointment(user_input):
    apointment_list = []
    projection_list = []
    for apointment in apointments:
        if user_input == apointment["date"].strip():
            for projection in projections:
                if projection['code'] in apointment['code']:
                    apointment_list.append(apointment)
                    projection_list.append(projection)
            print_table_projection(projection_list, apointment_list)
            input('Enter to continue...')
            return
    print('Unfortunaly there is no movie projection for that date.')
    return


def filter_movie_name(user_input, movie_name):
    return user_input.lower() == movie_name.lower()


def filter_cinema_hall(user_input, cinema_hall):
    return user_input.lower() == cinema_hall.lower()


def filter_starting_time(user_input, starting_time):
    starting_time = datetime.strptime(starting_time, "%H:%M")
    user_starting_time = datetime.strptime(user_input, "%H:%M")
    return starting_time == user_starting_time


def filter_ending_time(user_input, ending_time):
    ending_time = datetime.strptime(ending_time, "%H:%M")
    user_ending_time = datetime.strptime(user_input, "%H:%M")
    return ending_time == user_ending_time


choice_keys = {
    '1': 'movie name',
    '2': 'cinema hall',
    '3': 'date',
    '4': 'starting time',
    '5': 'ending time',

}

projection_filter_functions = {
    'movie name': filter_movie_name,
    'cinema hall': filter_cinema_hall,
    'date': check_date_apointment,
    'starting time': filter_starting_time,
    'ending time': filter_ending_time
}


def search_projection():
    while True:
        clear_screen1()
        print_table_projection(projections, apointments)
        print('Find the right movie for you by choosing: \n')
        print('1. Movie name')
        print('2. Cinema hall')
        print('3. Date')
        print('4. Starting time')
        print('5. Ending time')
        print('6. Back to the main manu')

        choice = input('Enter your choice: ')

        if choice == '6':
            clear_screen1()
            break
        elif choice == '':
            clear_screen1()
            print('Not existing choice. Try again.')
        elif choice in '12345':
            filter_projection(choice)
        else:
            clear_screen1()
            print('Not existing choice. Try again.')
