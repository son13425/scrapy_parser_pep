import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('a.pep.reference.internal::attr(href)')
        for all_pep in all_peps:
            yield response.follow(all_pep, callback=self.parse_pep)

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
