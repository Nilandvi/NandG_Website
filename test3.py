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
from data.notes import Note


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class NoteForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=255)])
    content = TextAreaField('Контент', validators=[DataRequired()])
    created_at = DateField('Дата создания', validators=[DataRequired()])
    user_id = IntegerField('ID пользователя', validators=[DataRequired(), NumberRange(min=1)])
    deadline = DateField('Дедлайн', validators=[Optional()])

def note(title, content, deathline):
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    note = Note(title=title, content=content, deathline=deathline)
    session.add(note)
    session.commit()

@app.route('/')
@app.route('/note', methods=['POST', 'GET'])
def notecreate():
    if request.method == 'GET':
      return render_template("note.html", title="Jinja and Flask")
    elif request.method == 'POST':
        note(request.form['title'], request.form['content'], request.form['deathline'])
        return "Форма отправлена и сохранена в базу данных"



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')