import time

from src.mapping import mysql_connection


def get_movie_data():
    file = open('../../ml-latest-small/data.csv', 'r', encoding='UTF-8')

    for data in file.readlines()[1:]:
        data = data.strip().split(',')
        user_id = data[0]
        rate = data[1]
        movie_id = data[2]
        title = data[3]

        yield {
            'userId': int(user_id),
            'rate': float(rate),
            'movieId': int(movie_id),
            'title': title
        }


def store_movie_data_to_db(movie, conn, cursor):
    select_sql = "SELECT * FROM movie_lens WHERE userId = %d AND movieId = %d" % (movie['userId'], movie['movieId'])

    try:
        cursor.execute(select_sql)
        result = cursor.fetchall()
    except:
        print("Failed to fetch data")

    if result.__len__() == 0:
        insert_sql = "INSERT INTO movie_lens (userId, rate, movieId, title) VALUES ('%d', '%f', '%d', '%s')" % \
                     (movie['userId'], movie['rate'], movie['movieId'],
                      movie['title'].replace("'", "‘"))

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
        for movie in get_movie_data():
            # print(movie)
            store_movie_data_to_db(movie, conn, cursor)
    finally:
        mysql_connection.close_conn(conn, cursor)


if __name__ == '__main__':
    main()
