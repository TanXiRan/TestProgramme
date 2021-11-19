# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DxdoctorPipeline:

    def __init__(self):
        self.f = open('./dxDoctor.txt', 'w')

    def process_item(self, item, spider):
        data = dict(item)
        ls = list()
        if data['cities']:
            for c in data['cities']:
                info = dict()
                del data['cities']
                info['provinceName'] = c['provinceName']
                info['currentConfirm'] = c['currentConfirmedCount']
                info['confirm'] = c['confirmedCount']
                info['death'] = c['deadCount']
                info['cure'] = c['curedCount']
                ls.append(info)
        for i in ls:
            self.f.write(item)
        return item

    def close_spider(self, spider):
        self.f.close()
