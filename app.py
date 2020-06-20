from flask import Flask, render_template, request
import scrapy
from scrapy.crawler import CrawlerRunner
import logging
from static.bin.job_scraper import JobsSpider
import json

crawl_runner = CrawlerRunner()
jobs_list = []
scrape_in_progress = False
scrape_complete = False

app = Flask('Job Description Scraper')

# boilerplate for testing
job_descriptions = [
  {
  "title": "Senior Data Scientist", 
  "company": "Jobot", 
  "description": "This Jobot Job is hosted by: Ellina Oganyan Are you a fit? Easy Apply now by clicking the \"Apply on compan"
  }
]

@app.route('/')
@app.route('/home')
def index():
  return render_template(
    'index.html', 
    job_descriptions=job_descriptions)

@app.route('/scrape')
def scrape_descriptions():
  global scrape_in_progress
  global scrape_complete

  if not scrape_in_progress:
    scrape_in_progress = True
    global jobs_list
    
    eventual = crawl_runner.crawl(
      JobsSpider, 
      jobs_list=jobs_list,
      title=request.args.get('title', None),
      location=request.args.get('location', None),
      pages=request.args.get('location', None)
    )

    eventual.addCallback(finished_scrape)
    return 'SCRAPING'
  elif scrape_complete:
    return 'SCRAPE COMPLETE'
  return 'SCRAPE IN PROGRESS'

@app.route('/results')
def get_results():
  global scrape_complete
  if scrape_complete:
    return json.dumps(jobs_list)
  return 'SCRAPING STILL IN PROGRESS'

def finished_scrape(null):
  global scrape_complete
  global scrape_in_progress
  scrape_complete = True
  scrape_in_progress = False


if __name__ == "__main__":
  from sys import stdout
  from twisted.logger import globalLogBeginner, textFileLogObserver
  from twisted.web import server, wsgi
  from twisted.internet import endpoints, reactor

  # start the logger
  globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

  logger = logging.getLogger(__name__)
  logging.basicConfig(level=logging.INFO)

  # start the WSGI server
  root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
  factory = server.Site(root_resource)
  http_server = endpoints.TCP4ServerEndpoint(reactor, 9000)
  http_server.listen(factory)

  # start event loop
  reactor.run()