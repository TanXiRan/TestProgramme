#!/usr/bin/env python3
# -*- coding=utf-8 -*-
from my_fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import pymysql
from pyecharts import options as opts
from pyecharts.charts import Map


def get_html(url):
    ua = UserAgent(family='chrome')
    res = ua.random()
    headers = {'user_agent': res}
    proxies = {'http://': '103.141.140.182:10003'}
    response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    try:
        if response.status_code == 200:
            response.encoding = 'gbk'
            return response.text
    except ConnectionError as ConnError:
        print(ConnError)


def get_info(html):
    soup = BeautifulSoup(html, features='lxml')
    trs = soup.body.find_all(attrs={'style': "mso-height-source:userset;height:18.0pt"})[5:37]
    lst = []
    for tr in trs:
        dataDict = dict()
        dataDict['region'] = tr.select("td[class^='xl5']")[0].text.replace('\xa0', '')
        population = [int(p.get_text()) for p in tr.select("td[class^='xl2']")[3:6]]
        dataDict['total'] = population[0]
        dataDict['male'] = population[1]
        dataDict['female'] = population[2]
        dataDict['ratio'] = float(tr.select("td[class^='xl3']")[0].text.replace(' ', ''))
        lst.append(dataDict)
    return lst


def createTable():
    connection = pymysql.connect(host='localhost', user='root', port=3306, password='tanhong')
    cursor = connection.cursor()
    create_db = "CREATE DATABASE IF NOT EXISTS stats_db DEFAULT CHARSET utf8 COLLATE utf8_general_ci;"
    cursor.execute(create_db)
    connection.select_db('stats_db')
    create_tbl = """CREATE TABLE stats_tbl(
        REGION VARCHAR(30) NOT NULL,
        POPULATION INT UNSIGNED NOT NULL,
        MALE INT UNSIGNED NOT NULL,
        FEMALE INT UNSIGNED NOT NULL,
        RATIO FLOAT NOT NULL
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
    cursor.execute(create_tbl)
    cursor.close()
    connection.close()
    print('创建数据库成功')


def write2sql(infos):
    infos = [tuple([i[key] for key in ['region', 'total', 'male', 'female', 'ratio']]) for i in infos]
    connection = pymysql.connect(host='localhost', user='root', port=3306, password='tanhong', db='stats_db')
    cursor = connection.cursor()
    insert_sql = "INSERT INTO stats_tbl values (%s,%s,%s,%s,%s);"
    rows = cursor.executemany(insert_sql, infos)
    print('插入了{}行'.format(rows))
    cursor.close()
    connection.commit()
    connection.close()
    print('写入数据库完成！')


def plot(infos):
    dataSeq1 = [[i[key] for key in ['region', 'total']] for i in infos[1:]]
    dataSeq2 = [[i[key] for key in ['region', 'ratio']] for i in infos[1:]]
    # [list(z) for z in zip([i['region'] for i in infos[1:]], [i['total'] for i in infos[1:]])]
    c = (
        Map()
        .add("各省总人口", dataSeq1, "china", is_selected=True)
        .add("各省男女比例", dataSeq2, "china", is_selected=False)
        .set_global_opts(title_opts=opts.TitleOpts(title="人口省份地图"),
                         legend_opts=opts.LegendOpts(selected_mode='single'),
                         visualmap_opts=opts.VisualMapOpts(max_=120000000, is_piecewise=True))
        .render("map_base.html")
    )


if __name__ == '__main__':
    html = get_html('http://www.stats.gov.cn/tjsj/pcsj/rkpc/6rp/html/A0101a.htm')
    lst = get_info(html)
    createTable()
    write2sql(lst)
    plot(lst)