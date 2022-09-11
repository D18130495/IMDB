import re
import pymysql
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

import mysql_connection


def get_top250_movies_list():
    url = "https://www.imdb.com/chart/top"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            movies = soup.select('tbody tr')

            for movie in movies:
                # movie name
                movie_name = movie.select_one('.titleColumn').select_one('a').string

                # movie score
                poster = movie.select_one('.posterColumn')
                movie_score = round(float(poster.select_one('span[name="ir"]')['data-value']), 1)

                # movie year
                year = movie.select_one('.titleColumn').select_one('span').get_text()
                movie_year_rule = re.compile('\d{4}')
                movie_year = int(movie_year_rule.search(year).group())

                # movie detail link
                movie_link = 'https://www.imdb.com/' + movie.select_one('.titleColumn').select_one('a')['href']

                # movie id from movie's link
                movie_id_rule = re.compile(r'(?<=tt)\d+(?=/?)')
                movie_id = int(movie_id_rule.search(movie_link).group())

                yield {
                    'movie_id': movie_id,
                    'movie_name': movie_name,
                    'year': movie_year,
                    'movie_score': float(movie_score),
                    'movie_link': movie_link
                }
        else:
            print("Error when request URL")
    except RequestException:
        print("Request Failed")
        return None


def store_movie_data_to_db(movie_data, conn, cursor):
    print(movie_data)
    select_sql = "SELECT * FROM top250_movies WHERE id = %d" % (movie_data['movie_id'])

    try:
        cursor.execute(select_sql)
        result = cursor.fetchall()
    except:
        print("Failed to fetch data")

    if result.__len__() == 0:
        insert_sql = "INSERT INTO top250_movies (id, name, year, score) VALUES ('%d', '%s', '%d', '%f')" % \
              (movie_data['movie_id'], movie_data['movie_name'], movie_data['year'], movie_data['movie_score'])

        try:
            cursor.execute(insert_sql)
            conn.commit()
            print("movie data ADDED to DB table top250_movies!")
        except:
            conn.rollback()
    else:
        print("This movie ALREADY EXISTED!!!")


def main():
    conn, cursor = mysql_connection.get_conn()

    try:
        for movie in get_top250_movies_list():
            store_movie_data_to_db(movie, conn, cursor)
    finally:
        mysql_connection.close_conn(conn, cursor)


if __name__ == '__main__':
    main()
