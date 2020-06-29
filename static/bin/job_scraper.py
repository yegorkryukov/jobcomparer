import scrapy
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class JobsSpider(scrapy.Spider):
    name = "jobs"

    def start_requests(self):
        pages = self.pages if self.pages else 1
        title = self.title if self.title else 'data scientist'
        location = self.location if self.location else '20001'

        urls = [
            'https://www.careerbuilder.com/jobs?keywords=%E2%80%9C'\
              + title \
              + '%E2%80%9D&location='\
              + location\
              + '&page_number='\
              + str(page) for page in range(1, pages + 1)
        ]
        for url in urls:
            logger.info(f'Processing URL: {url}')
            yield scrapy.Request(url=url, callback=self.parse)
        # !!!!!!!!!!!!!!!
            break # remove this line when finished debugging!!!!!
        # !!!!!!!!!!!!!!!

    def parse(self, response):
        # extract data in spider
        for a in response.xpath('//div[@id="jobs_collection"]//a[2]'):
            yield response.follow(a, self.parse_job)
    
    def parse_job(self, response):
        yield self.jobs_list.append({
            'title': response.xpath('//h1/text()').get(),
            'company' : response.xpath('//*[@id="jdp-data"]/div[1]/div[2]/div/div[1]/div[1]/span/text()').get(),
            'description': 
                ''.join(
                    s for s in \
                        ' '.join(response.xpath('//*[@id="jdp_description"]/div[1]/div[1]//text()')\
                        .extract())\
                        if s not in '\r\t\n\xa0'),
            'date_scraped': datetime.now().strftime('%Y-%m-%dT%R:%S')
        })