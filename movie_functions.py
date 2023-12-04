# U ovom fajlu se nalaze funcije koje omogucavaju korisnicima pretrage filmova.
import os


def clear_screen1():
    os.system('cls' if os.name == 'nt' else 'clear')


movies = []


def print_movies(number, movie):
    print(f'{number}. Name: {movie["name"]}\n'
          f'   Genre: {movie["genre"]}\n'
          f'   Duration(min): {movie["duration"]}\n'
          f'   Film director: {movie["film director"]}\n'
          f'   Main roles: {movie["actors"]}\n'
          f'   Country of production: {movie["country of production"]}\n'
          f'   Year of creation: {movie["year of production"]}\n'
          f'   Summary: {movie["summary"]}\n')


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
                'summary': movie[7]
            })


def avaliable_movies():
    clear_screen1()
    print('\n The movies we are currently showing: \n')
    num = 1
    for movie in movies:
        print_movies(num, movie)
        num += 1
    input('Enter to go back...')
    clear_screen1()


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
        for number, movie in enumerate(matching_movies, start=1):
            print_movies(number, movie)
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
        return movies


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

        categories_input = input('Enter the categories you want to search movies for (comma-separated): ')
        if '8' == categories_input:
            clear_screen1()
            break

        selected_categories = [category.strip() for category in categories_input.split(',')]

        invalid_categories = [category for category in selected_categories if category not in category_filter_functions]
        if invalid_categories:
            print(f'Invalid categories: {", ".join(invalid_categories)}. Please enter valid options.')
            continue
        search_by_categories(selected_categories)
