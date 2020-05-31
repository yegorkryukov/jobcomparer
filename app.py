from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__)

@app.route("/<string:name>")
def index(name):
  return render_template(
    'index.html', name=name)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)