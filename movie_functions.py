# U ovom fajlu se nalaze funcije koje omogucavaju korisnicima pretrage filmova.
import os
from datetime import datetime
from tabulate import tabulate


def clear_screen1():
    os.system('cls' if os.name == 'nt' else 'clear')


movies = []
apointments = []
projections = []


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
        table_data.append(table_row)

    table = tabulate(table_data, headers=headers, tablefmt='grid')
    print(table)


def read_movies():
    with open('movies.txt', 'r') as fin:
        for line in fin:
            movie = line.split('|')
            if movie[8] == 'active\n':
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


def avaliable_movies():
    clear_screen1()
    print('\n The movies we are currently showing: \n')
    print(movies)
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
        duration = input('Enter the duration of movie(in minutes): ')
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
            break
        for movie in movies:
            if movie['name'].lower() == name.lower():
                movie['status'] = 'deleted\n'
                write_movies()
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
            all_names.append(movie['name'].lower())

        if movie_name not in all_names:
            print('Your input does not match any movie, please try again.')
            continue

        code = input('Enter the 4-digit projection code: ')
        hall = input('Enter the cinema hall: ')
        starting_time = input('Enter the starting time: ')
        ending_time = input('Enter the ending time: ')
        days = input('Enter the days of projection: ')
        movie_name = input('Enter the movie name: ')
        price = input('Enter the starting price: ')

        days_list = days.split(',')

        if not all([code, hall, starting_time, ending_time, days, movie_name, price]):
            print("Please fill in all the data. None of the data can be empty. Try again.\n")
            continue

        with open('projections.txt', 'a') as fin:
            fin.write(code + '|' + hall + '|' + starting_time + '|' + ending_time + '|' + days + '|' +
                      movie_name + '|' + price + '\n')
        print('\nNew projection successfully added!')
        input('Enter to continue...')
        break

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
    return user_input.lower() in movie_actors


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
            })


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
                'price': proj[6]
            })


def print_table_projection(projection, appointment):
    headers = ["#", "Movie name", "Cinema hall", "Date of this projection", "Starting time", "Ending time"]
    table_data = []
    number = 1
    for appoint in appointment:
        for proj in projection:
            if proj['code'] in appoint['code']:
                table_row = [
                    number,
                    proj["movie name"],
                    proj["cinema hall"],
                    appoint["date"],
                    proj["starting time"],
                    proj["ending time"]
                ]
                table_data.append(table_row)
                number += 1
    table = tabulate(table_data, headers=headers, tablefmt="grid")
    print(table)


def filter_projection(choice):
    matching_projection = projections.copy()
    matching_appointment = []

    if choice == '3':
        clear_screen1()
        date_input = input(f'Write the date you are interested in: ')
        check_date_apointment(date_input)
        return
    elif choice in '12456':
        value = choice_keys[choice]
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
