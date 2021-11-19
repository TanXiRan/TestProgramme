#!/usr/bin/env python3
# -*- coding=utf-8 -*-
from my_fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import json
import csv
from pyecharts.charts import Bar
from pyecharts import options as opts


def get_html(url):
    ua = UserAgent(family='chrome')
    res = ua.random()
    headers = {'user_agent': res}
    proxies = {'http://': '103.141.140.182:10003'}
    response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    try:
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
    except ConnectionError as ConnError:
        print(ConnError)


def get_info(html):
    soup = BeautifulSoup(html, features='lxml')
    text_string = str(soup.body.find('script')).replace('{ window.getAreaStat = ', '{ "window.getAreaStat":')
    text = json.loads(text_string[text_string.index('try {')+4:text_string.index('catch(e){}</script>')], strict=False)
    info_list = list()
    for province in text['window.getAreaStat']:
        provinceRow = [province[p] for p in ['provinceName', 'currentConfirmedCount',
                                             'confirmedCount', 'deadCount', 'curedCount']]
        info_list.append(['provinceName', 'currentConfirm', 'confirm', 'death', 'cure'])
        info_list.append(provinceRow)
        if province['cities']:
            info_list.append(['cityName', 'currentConfirm', 'confirm', 'death', 'cure'])
            for city in province['cities']:
                cityRow = [city[c] for c in ['cityName', 'currentConfirmedCount',
                                             'confirmedCount', 'deadCount', 'curedCount']]
                info_list.append(cityRow)
    return info_list


def write2csv(info_list):
    print('开始写入....')
    with open('dxInfos2.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        for info in info_list:
            writer.writerow(info)
        print('写入完成....')


def plot(infos):
    bar1 = Bar()
    bar2 = Bar()
    bar3 = Bar()
    bar4 = Bar()
    bar1.add_xaxis(['currentConfirm', 'confirm', 'death', 'cure'])
    bar1.set_global_opts(title_opts=opts.TitleOpts(title='确诊人数超10000的省份柱状图'))
    bar2.add_xaxis(['currentConfirm', 'confirm', 'death', 'cure'])
    bar2.set_global_opts(title_opts=opts.TitleOpts(title='确诊人数超2000的省份柱状图'))
    bar3.add_xaxis(['currentConfirm', 'confirm', 'death', 'cure'])
    bar3.set_global_opts(title_opts=opts.TitleOpts(title='确诊人数超2000的省份柱状图'))
    bar4.add_xaxis(['currentConfirm', 'confirm', 'death', 'cure'])
    bar4.set_global_opts(title_opts=opts.TitleOpts(title='确诊人数小于1000的省份柱状图'))
    for i in infos:
        if i[2] > 10000:
            bar1.add_yaxis(i[0], i[1:])
        elif 2000 < i[2] <= 10000:
            bar2.add_yaxis(i[0], i[1:])
        elif 1000 < i[2] <= 2000:
            bar3.add_yaxis(i[0], i[1:])
        elif 0 < i[2] < 1000:
            bar4.add_yaxis(i[0], i[1:])
    bar1.render('bar1.html')
    bar2.render('bar2.html')
    bar3.render('bar3.html')
    bar4.render('bar4.html')


def main():
    html = get_html('http://ncov.dxy.cn/ncovh5/view/pneumonia')
    infos = get_info(html)
    write2csv(infos)
    plot(infos)


if __name__ == '__main__':
    main()
