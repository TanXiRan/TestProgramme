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
    for c in text['window.getAreaStat']:
        info = dict()
        info['provinceName'] = c['provinceName']
        info['currentConfirm'] = c['currentConfirmedCount']
        info['confirm'] = c['confirmedCount']
        info['death'] = c['deadCount']
        info['cure'] = c['curedCount']
        info_list.append(info)
        if c['cities']:
            for i in c['cities']:
                cityInfo = dict()
                # cityInfo['cityName'] = i['cityName']
                cityInfo['provinceName'] = i['cityName']
                cityInfo['currentConfirm'] = i['currentConfirmedCount']
                cityInfo['confirm'] = i['confirmedCount']
                cityInfo['death'] = i['deadCount']
                cityInfo['cure'] = i['curedCount']
                info_list.append(cityInfo)
    return info_list


def writeInfo(infos):
    print('开始写入....')
    with open('dxInfos.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['currentConfirm', 'confirm', 'death', 'cure'])
        for info in infos:
            writer.writerow([i for i in info.values()])
    print('写入完成....')


def plot(infos):
    bar = Bar()
    bar.add_xaxis(['currentConfirm', 'confirm', 'death', 'cure'])
    for i in infos[:5]:
        bar.add_yaxis(i['provinceName'], [i['currentConfirm'], i['confirm'], i['death'], i['cure']])
    bar.render('dx.html')


h = get_html('http://ncov.dxy.cn/ncovh5/view/pneumonia')
infos = get_info(h)
# writeInfo(infos)
plot(infos)
