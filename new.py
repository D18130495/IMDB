import re
import time
import traceback

from bs4 import BeautifulSoup
from lxml import etree
import pymysql
import requests


def get_conn():
    conn = pymysql.connect(host="47.241.6.156", user="root", password="qpuur990415", db="personal_blog", charset="utf8")

    cursor = conn.cursor()
    if (conn is not None) & (cursor is not None):
        print("数据库连接成功！游标创建成功！")
    else:
        print("数据库连接失败！")
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        return 1


def get_imdb():
    # url = 'https://www.imdb.cn/feature-film/1-0-0-0/?page=1'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.93 Safari/537.36 '
    }

    dataRes = []
    temp_list = []

    url_ = 'https://www.imdb.com/chart/top/'
    response = requests.get(url=url_, headers=headers)
    response.encoding = 'utf-8'
    page_text = response.text
    etree_ = etree.HTML(page_text)
    all_li = etree_.xpath('//div[@class="hot_box"]/ul/li')
    # 判断all_li是否为空
    print(all_li)
    # if len(all_li) == 0:
    #     print("爬取结束，all_list为空！")
    #     if len(dataRes) != 0:
    #         return dataRes
    #     else:
    #         return
    # print(url_)


#  62             for li in all_li:
#  63                 name=li.xpath('./a[1]/img/@alt')
#  64                 if(len(name)==0):
#  65                     name.append("电影名错误")
#  66                 # print(name)
#  67                 #存姓名
#  68                 temp_list.append(name[0])
#  69
#  70                 score=li.xpath('./span[@class="img_score"]/@title')
#  71                 if(len(score)==0):
#  72                     score.append("imdb暂无评分")
#  73                 # print(score)
#  74                 #存分数
#  75                 temp_list.append(score[0])
#  76                 # print(temp_list)
#  77                 #存到dataRes 把temp_list置为空
#  78                 dataRes.append(temp_list)
#  79                 temp_list=[]
#  80             print(dataRes)
#  81     return dataRes
#  82 def insert_imdb():
#  83     """
#  84         插入imdb数据
#  85         :return:
#  86         """
#  87     cursor = None
#  88     conn = None
#  89     try:
#  90         list_=[]
#  91         list = get_imdb()
#  92         if(type(list)!=type(list_)):
#  93             return ;
#  94         print(f"{time.asctime()}开始插入imdb数据")
#  95         conn, cursor = get_conn()
#  96         sql = "insert into movieimdb (id,name,score) values(%s,%s,%s)"
#  97         for item in list:
#  98             try:
#  99                 print(item)
# 100                 cursor.execute(sql, [0, item[0], item[1]])
# 101             except pymysql.err.IntegrityError:
# 102                 print("重复！跳过！")
# 103             conn.commit()  # 提交事务 update delete insert操作
# 104             print(f"{time.asctime()}插入imdb数据完毕")
# 105     finally:
# 106         close_conn(conn, cursor)
# 107     return;
# 108 # def get_dblen():
# 109 #     conn,cursor=
# 110 #     num_=

if __name__ == '__main__':
    get_imdb()
#     insert_imdb()
