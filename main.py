from flask import Flask, render_template, request, url_for, redirect
from data import db_session
from data.users import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def find_user_by_id(user_id):
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    return user


def find_user_by_nickname(nickname):
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    user = session.query(User).filter(User.nickname == nickname).first()
    return user


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


@app.route('/autorization', methods=['POST', 'GET'])
def authorization_form_sample():
    if request.method == 'GET':
        return render_template("autorization.html", title="Jinja and Flask")
    elif request.method == 'POST':
        nickname = request.form['username']
        password = request.form['password']
        if not nickname or not password:
            return "Nickname and password are required"
        user = find_user_by_nickname(nickname)
        if user and user.hashed_password == password:
            return redirect(url_for('account', user_id=user.id))
        return "Invalid nickname or password"


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return render_template("registration.html", title="Jinja and Flask")
    elif request.method == 'POST':
        nickname = request.form['nickname']
        name = request.form['name']
        about = request.form['about']
        email = request.form['mail']
        password = request.form['password']
        user = find_user_by_nickname(nickname)
        if user:
            return "User with this nickname already exists"
        register(nickname, name, about, email, password)
        return redirect(url_for('authorization_form_sample'))


@app.route('/account/<int:user_id>')
def account(user_id):
    user = find_user_by_id(user_id)
    if user:
        return render_template('account.html', title='Account', user=user)
    else:
        return "User not found"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
