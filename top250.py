from urllib import request
from chardet import detect
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


def get_soup(url):
    with request.urlopen(url) as fp:
        byt = fp.read()
        det = detect(byt)
        time.sleep(random.randrange(1, 5))
        return BeautifulSoup(byt.decode(det['encoding']))


def get_data(soup):
    # 获取评分
    ol = soup.find('tbody', attrs={'class': 'lister-list'})
    score_info = ol.find_all('td', attrs={'class': 'imdbRating'})
    film_scores = [k.text.replace('\n', '') for k in score_info]
    # 获取评分、电影名、导演・演员、上映年份、详情网页链接
    film_info = ol.find_all('td', attrs={'class': 'titleColumn'})
    film_names = [k.find('a').text for k in film_info]
    film_actors = [k.find('a').attrs['title'] for k in film_info]
    film_years = [k.find('span').text[1:5] for k in film_info]
    # next_nurl = [url2 + k.find('a').attrs['href'][0:17] for k in film_info] , 'newurl': next_nurl
    data = pd.DataFrame(
        {'name': film_names, 'year': film_years, 'score': film_scores, 'actors': film_actors})
    return data


def next_url(detail, detail1):
    # 获取电影国家
    detail_list = detail.find('div', attrs={'id': 'titleDetails'}).find_all('div', attrs={'class': 'txt-block'})
    detail_str = [k.text.replace('\n', '') for k in detail_list]
    detail_str = [k for k in detail_str if k.find(':') >= 0]
    detail_dict = {k.split(':')[0]: k.split(':')[1] for k in detail_str}
    country = detail_dict['Country']
    # 获取电影类型
    detail_list1 = detail.find('div', attrs={'class': 'title_wrapper'}).find_all('div', attrs={'class': 'subtext'})
    detail_str1 = [k.find('a').text for k in detail_list1]
    movie_type = pd.DataFrame({'Type': detail_str1})
    # 获取以组划分的电影详细评分、人数
    div_list = detail1.find_all('td', attrs={'align': 'center'})
    value = [k.find('div', attrs={'class': 'bigcell'}).text.strip() for k in div_list]
    num = [k.find('div', attrs={'class': 'smallcell'}).text.strip() for k in div_list]
    scores = pd.DataFrame({'value': value, 'num': num})
    return country, movie_type, scores


if __name__ == '__main__':
    IMDB = get_soup("https://www.imdb.com/chart/top/")
    print(get_data(IMDB))
