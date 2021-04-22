from sqlite3.dbapi2 import IntegrityError
from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.utils import redirect
from data import db_session, db_models

from data.db_models import User, Check, Expenses
import forms
import smtplib


app = Flask(__name__)
app.config['SECRET_KEY'] = 'check_check_key'

db_session.global_init('web_db.sqlite')
login_manager = LoginManager(app)
login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def send_mail(msg, tomail):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('pweb2800@gmail.com', '123YlWeb')
    smtpObj.sendmail(smtpObj.user, tomail, msg)
    smtpObj.quit()


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User(form.name.data, form.email.data,
                    form.password.data, form.inn.data)
        try:
            db_sess.add(user)
            db_sess.commit()
            send_mail("Поздравляем, вы зарегистрировались в CheckЧек!", form.email)
        except IntegrityError:
            return render_template("registration.html", title="Регистрация", form=form,
                                   message='Данная электронная почта уже зарегистрирована.')
        except Exception:
            return render_template("registration.html", title="Регистрация", form=form,
                                   message='Произошла неизвестная ошибка.')
        finally:
            db_sess.close()
            return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', title="Авторизация", form=form)
    return render_template('login.html', title="Авторизация", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/add_new_check', methods=['GET', 'POST'])
@login_required
def add_new_check():
    form = forms.AddCheckForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        check = Check(form.str_Qr.data, form.id_type.data,
                      form.description.data, form.information.data)
        current_user.checks.append(check)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_new_check.html', title="Добавление нового чека", form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
