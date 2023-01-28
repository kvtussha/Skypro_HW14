import sqlite3


def search_name(title):
    """Поиск по названию"""
    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        query = """
               SELECT title, country, release_year, listed_in, description
               FROM netflix
               WHERE title = ?
        """

        result = cur.execute(query, (title,)).fetchone()
        return {
            "title": result[0],
            "country": result[1],
            "release_year": result[2],
            "genre": result[3],
            "description": result[4].strip()
        }


def movie_year(year1, year2):
    """Поиск фильмов по диапазону годов"""
    with sqlite3.connect("netflix.db") as con:
        cursor = con.cursor()
        query = """
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN ? AND ?
        """
    result = cursor.execute(query, (year1, year2,)).fetchall()
    res_list = []
    for i in range(len(result)):
        res_list.append({
            "title": result[i][0],
            "release_year": result[i][1]
        })
    return res_list


def search_rating(rating):
    """Поиск по рейтингу"""
    with sqlite3.connect("netflix.db") as con:
        cursor = con.cursor()
        query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating IN {rating}
            """

    result = cursor.execute(query).fetchall()
    res_list = []
    for i in range(len(result)):
        res_list.append({"title": result[i][0],
                         "rating": result[i][1],
                         "description": result[i][2]
                         })
    return res_list


def search_genre(listed_in):
    """Поиск по жанру"""
    with sqlite3.connect('netflix.db') as con:
        cur = con.cursor()
        query = """
                SELECT title, description, listed_in, release_year
                FROM netflix
                WHERE listed_in LIKE ?
                ORDER BY release_year DESC
                LIMIT 10    
        """

    result = cur.execute(query, ('%' + listed_in + '%',)).fetchall()
    res_list = []
    for i in range(len(result)):
        res_list.append({
            "title": result[i][0],
            "description": result[i][1],
        })
    return res_list


def type_year_genre(type_, release_year, listed_in):
    """Передает тип картины, год выпуска и ее жанр и получает список с названиями и описаниями"""
    with sqlite3.connect('netflix.db') as con:
        cur = con.cursor()
        query = """
                SELECT title, description
                FROM netflix
                WHERE  type = ?
                AND release_year = ?
                AND listed_in LIKE ? 
                LIMIT 15
        """
    result = cur.execute(query, (type_, release_year, '%' + listed_in + '%',)).fetchall()
    res_list = []
    for i in range(len(result)):
        res_list.append({
            "title": result[i][0],
            "description": result[i][1]
        })
    return res_list


# print(type_year_genre('Movie', 1944, 'Classic Movies'))

def actors(actor1, actor2):
    with sqlite3.connect('netflix.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        query = """
                SELECT "cast"
                FROM netflix
                WHERE "cast" LIKE ? AND "cast" LIKE ?
        """
    result = cur.execute(query, ('%' + actor1 + '%', '%' + actor2 + '%')).fetchall()
    actors = {}
    actors_list = []

    for i in result:
        for actor_names in i:
            for name in actor_names.split(', '):
                if name in actors:
                    actors[name] += 1
                else:
                    actors[name] = 1
    for k, v in actors.items():
        if v > 2 and k != actor1 and k != actor2:
            actors_list.append(k)
    return actors_list

# print(actors('Rose McIver', 'Ben Lamb'))