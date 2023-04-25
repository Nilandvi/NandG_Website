from flask import Flask, render_template, request, url_for, redirect
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def register(nickname, name, about, mail, password):
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    user = User(nickname=nickname, name=name, about=about, email=mail, hashed_password=password)
    session.add(user)
    session.commit()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Jinja and Flask")

@app.route('/')
@app.route('/autorization', methods=['POST', 'GET'])
def autorization_form_sample():
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    if request.method == 'GET':
      return render_template("autorization.html", title="Jinja and Flask")
    elif request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        return redirect(url_for('account', number=3))

@app.route('/')
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'GET':
      return render_template("registration.html", title="Jinja and Flask")
    elif request.method == 'POST':
        register(request.form['nickname'], request.form['name'], request.form['about'], request.form['mail'], request.form['password'])
        print(request.form['nickname'], request.form['name'], request.form['about'], request.form['mail'], request.form['password'])
        return redirect((url_for('autorization_form_sample')))


@app.route('/account/<number>')
def account(number):
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    user = session.query(User).filter(User.id == int(number)).first()
    return render_template('account.html', title='Account', user=user)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')