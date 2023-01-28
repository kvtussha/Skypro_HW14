from flask import Flask, request, render_template
from functions import search_name, search_rating, movie_year, search_genre

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/movie/title')
def search_name_():
    title = request.args.get('title')
    film = search_name(title)
    return render_template('title_search.html', film=film)


@app.route('/movie/year_to_year')
def search_by_year():
    query1 = request.args.get('from_year')
    query2 = request.args.get('to_year')
    films = movie_year(query1, query2)
    return render_template('search_year.html', films=films)

@app.route('/rating/<rating>')
def rating_(rating):
    if rating == 'children':
        rating = 'G'
    elif rating == 'family':
        rating = ('G', 'PG', 'PG-13')
    elif rating == 'adult':
        rating = ('R', 'NC-17')
    films = search_rating(rating)
    return render_template('search_rating.html', films=films)


@app.route('/genre/genre')
def search_by_genre():
    query = request.args.get('genre')
    films = search_genre(query)
    return render_template('search_genre.html', films=films)


app.run()