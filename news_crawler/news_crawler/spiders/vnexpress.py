#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import os
import json
from codecs import open
from datetime import datetime
import re

URL = 'https://vnexpress.net/'

CATEGORIES = {
    'kinh-doanh': 'Kinh doanh',
    'khoa-hoc': 'Khoa học',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'phap-luat': 'Pháp luật',
    'giao-duc': 'Giáo dục',
    'suc-khoe': 'Sức khoẻ - Y tế',
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch'
}

CATEGORIES_COUNTER = {
    'kinh-doanh': [0,2000],
    'khoa-hoc': [0,2000],
    'giai-tri': [0,2000],
    'the-thao': [0,2000],
    'phap-luat': [0,2000],
    'giao-duc': [0,2000],
    'suc-khoe': [0,2000],
    'doi-song': [0,2000],
    'du-lich': [0,2000]
}

class VnExpress(scrapy.Spider):
    name = "vnexpress"
    folder_path = "vnexpress"
    page_count = 0
    page_limit = None
    category = ""
    start_urls = [
    ]

    def __init__(self, category=None, limit=None, *args, **kwargs):
        super(VnExpress, self).__init__(*args, **kwargs)
        self.count = 0
        self.category = category
        if limit != None:
            self.page_limit = int(limit)
        # Tạo thư mục
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

        if category in CATEGORIES:
            folders_path = self.folder_path + '/' + CATEGORIES[category]
            if not os.path.exists(folders_path):
                os.makedirs(folders_path)
            self.start_urls = [URL + category]
            
        else:
            for CATEGORY in CATEGORIES:
                folders_path = self.folder_path + '/' + CATEGORIES[CATEGORY]
                if not os.path.exists(folders_path):
                    os.makedirs(folders_path)
                self.start_urls.append(URL + CATEGORY)
    def parse(self, response):

        if self.page_limit is not None:
            if self.page_count > self.page_limit:
                return
        next_page = response.css('div.button-page a.next-page::attr(href)').get()

        if next_page is not None:
            self.page_count += 1
            yield response.follow(next_page, callback=self.parse)
        labels= response.url.split('/')[-1].split('-')
        if len(labels) < 2:
            return
        self.label = labels[0]+'-'+labels[1]
        for paper_href in response.css('p.description a::attr(href)'):
            if paper_href is not None:
                
                yield response.follow(paper_href, self.get)

    def get(self, response):
        jsonData = self.extract_news(response)
        yield jsonData
        if jsonData is not None:
            CATEGORIES_COUNTER[jsonData['label']][0] = CATEGORIES_COUNTER[jsonData['label']][0] + 1
            if (CATEGORIES_COUNTER[jsonData['label']][0] <= CATEGORIES_COUNTER[jsonData['label']][1]):
                filename = '%s/%s-%s.json' % (CATEGORIES[jsonData['label']], CATEGORIES[jsonData['label']], CATEGORIES_COUNTER[jsonData['label']][0])
                with open(self.folder_path + "/" + filename, 'wb', encoding = 'utf-8') as fp:
                    json.dump(jsonData, fp, ensure_ascii= False)
                    print(self.folder_path + "/" + filename)
            else:
                return
        # with open(self.folder_path + "/" + "the-thao.json", 'wb', encoding = 'utf-8') as fp:
        #     json.dump(jsonData, fp, ensure_ascii= False)
    

    def extract_news(self, response):
        content = response.css('div.sidebar-1')
        if content.css('h1.title-detail::text').get() is not None:
            copurs =""
            for paragraph in response.css('article.fck_detail p.Normal::text').getall():
                copurs+=paragraph+" "
          
            jsonData = {
                'label': self.label,
                'link': response.url,
                'title':content.css('h1.title-detail::text').get(),
                'description':content.css('p.description::text').get(),
                'content':copurs
            }
            return jsonData
