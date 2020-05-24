import scrapy


class QuotesSpider(scrapy.Spider):
    name = "jobs"

    

    def start_requests(self):
        pages = 16
        urls = [
            'https://www.careerbuilder.com/jobs?keywords=%E2%80%9Cdata+scientist%E2%80%9D&location=20005&page_number=' + str(page) for page in range(1, pages + 1)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # extract data in spider
        for a in response.xpath('//div[@id="jobs_collection"]//a[2]'):
            yield response.follow(a, self.parse_job)
    
    def parse_job(self, response):
        yield {
            'title': response.xpath('//h1/text()').get(),
            'company' : response.xpath('//*[@id="jdp-data"]/div[1]/div[2]/div/div[1]/div[1]/span/text()').get(),
            'description': 
                ''.join(
                    s for s in \
                        ' '.join(response.xpath('//*[@id="jdp_description"]/div[1]/div[1]//text()')\
                        .extract())\
                        if s not in '\r\t\n\xa0')
        }