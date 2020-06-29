from flask import Flask, render_template, request, redirect, Response
import scrapy
from scrapy.crawler import CrawlerRunner
import logging
from static.bin.job_scraper import JobsSpider
import json
import time
from datetime import datetime

crawl_runner = CrawlerRunner()
jobs_list = []
scrape_in_progress = False
scrape_complete = False

app = Flask('Job Description Scraper')

# boilerplate for testing
job_descriptions = []

@app.route('/')
@app.route('/home')
def index():
  global scrape_complete
  global jobs_list

  return render_template('index.html')

@app.route('/scrape')
def descriptions_data():
  def scrape_data():
    global scrape_in_progress
    global scrape_complete
    global jobs_list

    if not scrape_in_progress:
      scrape_in_progress = True

      json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
      print(json_data)
      yield f"data:{json_data}\n\n"
      time.sleep(1)
      scrape_in_progress = False

  return Response(scrape_data(), mimetype='text/event-stream')
      
  #     eventual = crawl_runner.crawl(
  #       JobsSpider, 
  #       jobs_list=jobs_list,
  #       title=request.args.get('title', None),
  #       location=request.args.get('location', None),
  #       pages=request.args.get('location', None)
  #     )

  #     eventual.addCallback(finished_scrape)
    
  # def finished_scrape(null):
  #   global scrape_in_progress
  #   global scrape_complete
  #   global jobs_list
  #   scrape_complete = True
  #   scrape_in_progress = False
  #   print(f'/index: SIP: {scrape_in_progress}, SC: {scrape_complete}')
  #   data = json.dumps(jobs_list)
  #   print(data)
  #   yield f'data:{data}\n\n'
    
  # return Response(scrape_data(), mimetype='text/event-stream')
    



if __name__ == "__main__":
  reactor_args = {}

  def run_twisted_wsgi():
    from sys import stdout
    from twisted.logger import globalLogBeginner, textFileLogObserver
    from twisted.web import server, wsgi
    from twisted.internet import endpoints, reactor

    # start the logger
    globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    # logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    # start the WSGI server
    root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    factory = server.Site(root_resource)
    http_server = endpoints.TCP4ServerEndpoint(reactor, 5000)
    http_server.listen(factory)

    # start event loop
    reactor.run(**reactor_args)

  if app.debug:
    # Disable twisted signal handlers in development only.
    reactor_args['installSignalHandlers'] = 0
    # Turn on auto reload.
    import werkzeug.serving
    run_twisted_wsgi = werkzeug.serving.run_with_reloader(run_twisted_wsgi)
  run_twisted_wsgi()