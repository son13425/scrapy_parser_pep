import re
from urllib.parse import urljoin

import scrapy

from pep_parse.items import PepParseItem

BASE_URL = 'https://peps.python.org/'


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = [BASE_URL]

    def parse(self, response):
        table = response.xpath('//*[@id="numerical-index"]').css('tbody')
        all_peps = table.css('a::attr(href)').getall()
        for all_pep in all_peps:
            version_link = urljoin(BASE_URL, all_pep + '/')
            yield response.follow(version_link, callback=self.parse_pep)

    def parse_pep(self, response):
        number_name = response.css('h1.page-title::text').get()
        pattern = r'PEP (?P<number>\d+) – (?P<name>.*)'
        text_match = re.search(pattern, number_name)
        number, name = text_match.groups()
        status_tag = response.css('dt:contains("Status") + dd')
        status = status_tag.css('abbr::text').get()
        data = {
            'number': number,
            'name': name,
            'status': status
        }
        yield PepParseItem(data)
