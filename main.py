from flask import Flask

app = Flask(__name__)

us = {"usir": "ТЕЕЕЕЕЕЕЕЕЕЕЕЕСТ"}
@app.route('/')
@app.route('/index')
def index():
    return "геншин инфаркт " + str(us["usir"])


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')