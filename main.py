from flask import Flask, render_template, request, url_for, redirect
from data import db_session
from data.users import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from data.news import Note


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class NoteForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=255)])
    content = TextAreaField('Контент', validators=[DataRequired()])
    created_at = DateField('Дата создания', validators=[DataRequired()])
    user_id = IntegerField('ID пользователя', validators=[DataRequired(), NumberRange(min=1)])
    deadline = DateField('Дедлайн', validators=[Optional()])

def register(nickname, name, about, mail, password):
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    user = User(nickname=nickname, name=name, about=about, email=mail, hashed_password=password)
    session.add(user)
    session.commit()

def note(title, content, deathline):
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    note = Note(title=title, content=content, deathline=deathline)
    session.add(note)
    session.commit()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Jinja and Flask")

@app.route('/')
@app.route('/autorization', methods=['POST', 'GET'])
def autorization_form_sample():
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

@app.route('/')
@app.route('/note', methods=['POST', 'GET'])
def notecreate():
    if request.method == 'GET':
      return render_template("note.html", title="Jinja and Flask")
    elif request.method == 'POST':
        register(request.form['title'], request.form['content'], request.form['deathline'])
        return "Форма отправлена и сохранена в базу данных"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')