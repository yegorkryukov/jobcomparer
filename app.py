from flask import Flask, render_template, request

app = Flask(__name__)

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
  title = request.args.get('title', None)
  if title: return title
  return 'no title provided'

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)