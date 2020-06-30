from flask import Flask, render_template, request, redirect, Response, jsonify
from flask_restful import Resource, Api, reqparse
import scrapy
from scrapy.crawler import CrawlerRunner
import logging
from static.bin.job_scraper import JobsSpider
import json
import time
from datetime import datetime

# crawl_runner = CrawlerRunner()
jobs_list = [{'title':'this is dummy title for debugging'}]
# scrape_in_progress = False
# scrape_complete = False

app = Flask('Job Description Scraper')
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('job_title')

class JobsAPI(Resource):
  def post(self):
    args = parser.parse_args()
    print(args)
    return jsonify(args)
  
  def get(self):
    print('get is working')
    return ''

api.add_resource(JobsAPI, '/jobs')

@app.route('/')
@app.route('/home')
def index():
  return render_template('index.html')





      
  #     eventual = crawl_runner.crawl(
  #       JobsSpider, 
  #       jobs_list=jobs_list,
  #       title=request.args.get('title', None),
  #       location=request.args.get('location', None),
  #       pages=request.args.get('location', None)
  #     )

  #     eventual.addCallback(finished_scrape)
    

    



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