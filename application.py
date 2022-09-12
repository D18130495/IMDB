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
                    'movie_year': movie_year,
                    'movie_score': float(movie_score),
                    'movie_link': movie_link
                }
        else:
            print("Error when request URL")
    except RequestException:
        print("Request Failed")
        return None


def store_movie_data_to_db(movie_data, conn, cursor):
    select_sql = "SELECT * FROM top250_movies WHERE id = %d" % (movie_data['movie_id'])

    try:
        cursor.execute(select_sql)
        result = cursor.fetchall()
    except:
        print("Failed to fetch data")

    if result.__len__() == 0:
        movie_name = movie_data['movie_name']

        insert_sql = "INSERT INTO top250_movies (id, name, year, score) VALUES ('%d', '%s', '%d', '%f')" % \
                     (movie_data['movie_id'], movie_data['movie_name'].replace("'", "‘"), movie_data['movie_year'],
                      movie_data['movie_score'])

        try:
            cursor.execute(insert_sql)
            conn.commit()
            print("movie data ADDED to DB table top250_movies!")
        except:
            conn.rollback()
    else:
        print("This movie ALREADY EXISTED!!!")


def get_movie_detail_data(movie_data, conn, cursor):
    url = movie_data['movie_link']

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            director = soup.select_one('div[class="ipc-metadata-list-item__content-container"]')
            # directors = soup.select('span:-soup-contains("Director")')

            director_link = director.select_one('a')['href']
            director_name = director.select_one('a').string
            director_id_rule = re.compile(r'(?<=nm)\d+(?=/?)')
            director_id = int(director_id_rule.search(director_link).group())

            movie_data['director_id'] = director_id
            movie_data['director_name'] = director_name.string

            store_director_data_in_db(movie_data, conn, cursor)
        #         #parse Cast's data
        #         cast = soup.select('table.cast_list tr[class!="castlist_label"]')
        #         for actor in get_cast_data(cast):
        #             store_actor_data_to_db(actor, movie_data)
        else:
            print("GET url of movie Do Not 200 OK!")
    except RequestException:
        print("Get Movie URL failed!")
        return None


def store_director_data_in_db(movie, conn, cursor):
    sel_sql = "SELECT * FROM directors WHERE id = %d" % (movie['director_id'])

    try:
        cursor.execute(sel_sql)
        result = cursor.fetchall()
    except:
        print("Failed to fetch data")

    if result.__len__() == 0:
        sql = "INSERT INTO directors (id, name) VALUES ('%d', '%s')" % (movie['director_id'], movie['director_name'])

        try:
            cursor.execute(sql)
            conn.commit()
            print("Director data ADDED to DB table directors!", movie['director_name'])
        except:
            conn.rollback()
    else:
        print("This Director ALREADY EXISTED!!")

    sel_sql = "SELECT * FROM direct_movie WHERE director_id = %d AND movie_id = %d" % \
              (movie['director_id'], movie['movie_id'])

    try:
        cursor.execute(sel_sql)
        result = cursor.fetchall()
    except:
        print("Failed to fetch data")

    if result.__len__() == 0:
        sql = "INSERT INTO direct_movie (director_id, movie_id) VALUES ('%d', '%d')" % \
              (movie['director_id'], movie['movie_id'])
        try:
            cursor.execute(sql)
            conn.commit()
            print("Director direct movie data ADD to DB table direct_movie!")
        except:
            conn.rollback()
    else:
        print("This Director direct movie ALREADY EXISTED!!!")


def main():
    conn, cursor = mysql_connection.get_conn()

    try:
        for movie in get_top250_movies_list():
            # print(movie)
            store_movie_data_to_db(movie, conn, cursor)
            get_movie_detail_data(movie, conn, cursor)
    finally:
        mysql_connection.close_conn(conn, cursor)


if __name__ == '__main__':
    main()
