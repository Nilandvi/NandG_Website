from flask import Flask
from data import db_session
from data.users import User
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    user = User(name="Анатолий", about="программист") #создали
    #session.add(user) #добавляю юзера
    #session.commit() #сохраняю юзера
    users = session.query(User).where(User.name == "Анатолий").first() #фильтрую юзера Анатолий ((Первый антон!)) (((можно юзать либо filter, либо where)))
    #for user in users:
    #    print(user.name)
    print(users.name, users.about)
    #импорт из sql если несколько, в лекции есть

if __name__ == '__main__':
    main()