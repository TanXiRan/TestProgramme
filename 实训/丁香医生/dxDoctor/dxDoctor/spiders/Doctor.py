import scrapy
from bs4 import BeautifulSoup
import json
from 实训.丁香医生.dxDoctor.dxDoctor.items import DxdoctorItem
from scrapy import cmdline


class DoctorSpider(scrapy.Spider):
    name = 'Doctor'
    allowed_domains = ['ncov.dxy.cn']
    start_urls = ['http://ncov.dxy.cn/ncovh5/view/pneumonia']

    def parse(self, response):
        soup = BeautifulSoup(response.text, features='lxml')
        s = str(soup.body.find('script')).replace('{ window.getAreaStat = ', '{ "window.getAreaStat":')
        infos = json.loads(s[s.index('try {') + 4:s.index('catch(e){}</script>')], strict=False)['window.getAreaStat']
        for i in infos:
            # print(i)
            item = DxdoctorItem()
            # info = list()
            # info.append(i['provinceName'])
            # info.append(i['currentConfirmedCount'])
            # info.append(i['confirmedCount'])
            # info.append(i['deadCount'])
            # info.append(i['curedCount'])
            # item['info'] = info
            yield item


cmdline.execute('scrapy crawl Doctor'.split())