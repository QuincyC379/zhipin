# -*- coding: utf-8 -*-
import re

import scrapy

from zhipin.items import ZhipinItem


class BossZhipinSpider(scrapy.Spider):
    name = 'boss_zhipin'
    allowed_domains = ['https://www.zhipin.com']
    url = 'https://www.zhipin.com/c101020100/h_101020100/?query=python&page=%s'
    offset = 1
    start_urls = [url % offset]

    # https: // www.zhipin.com / c101020100 / h_101020100 /?query = python & page = 1
    # https: // www.zhipin.com / c101020100 / h_101020100 /?query = python & page = 10

    def parse(self, response):
        item = ZhipinItem()
        for response_part in response.css('#main > div > div.job-list > ul').extract():
            company_size = []
            company_info = re.findall('<em class="vline"></em>(.*?)</p>', response_part)
            # 算出列表长度，拿到偶数位的数据
            # for idx in range(1, len(company_info)+1, 2):
            for idx, val in enumerate(company_info):
                if int(idx) % 2 != 0:
                    if '<em class="vline"></em>' in company_info[idx]:
                        new_item = company_info[idx].rsplit('</em>')[-1]
                        company_size.append(new_item)
                    else:
                        # 没带</em>直接加到company_size中
                        company_size.append(company_info[idx])
            result = zip(re.findall('title">(.*?)</div>', response_part),
                         re.findall('<span class="red">(.*?)</span>', response_part),
                         re.findall('ka="search_list_company_\d+_custompage" target="_blank">(.*?)</a>', response_part),
                         company_size,
                         re.findall('发布于(.*?)</p>', response_part))
            for job_item in result:
                """
                处理元组数据，返回item
                """
                item['job_title'] = job_item[0]
                item['job_salary'] = job_item[1]
                item['job_company'] = job_item[2]
                item['company_size'] = job_item[3]
                item['publish_date'] = job_item[4]
                yield item

        if self.offset < 10:
            self.offset += 1
            yield scrapy.Request(self.url % self.offset, callback=self.parse, dont_filter=True)
