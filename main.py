import os
from sqlite3.dbapi2 import IntegrityError
from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, user_logged_in
from werkzeug.utils import redirect
from data import db_session

from data.db_models import User, Check, Type
import forms
import smtplib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'check_check_key'

db_session.global_init('web_db.sqlite')
login_manager = LoginManager(app)
login_manager.login_view = '/login'

db_sess = db_session.create_session()
TYPE = db_sess.query(Type).all()


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(form.name.data, form.email.data, form.password.data, form.inn.data)
        try:
            db_sess.add(user)
            db_sess.commit()
            global MAIL
            MAIL = user.email,
        except IntegrityError:
            return render_template("registration.html", title="Регистрация", form=form,
                                   message='Данная электронная почта уже зарегистрирована.')
        except Exception:
            return render_template("registration.html", title="Регистрация", form=form,
                                   message='Произошла неизвестная ошибка.')
        finally:
            return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/personal_account')  # в личный кобинет
        return render_template('login.html', title="Авторизация", form=form)
    return render_template('login.html', title="Авторизация", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/add_new_check', methods=['GET', 'POST'])
@login_required
def add_new_check():
    form = forms.AddCheckForm()
    if form.validate_on_submit():
        check = Check(form.adress.data, form.id_type.data,
                      form.information.data, current_user.get_id(), form.price.data)
        current_user.checks.append(check)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')  # страница всех чеков пользователя
    return render_template('add_new_check.html', title="Добавление нового чека", form=form)


@app.route('/add_new_type', methods=['GET', 'POST'])
@login_required
def add_new_type():
    form = forms.CreateTypeForm()
    if form.validate_on_submit():
        type = Type(form.name.data)
        try:
            db_sess.add(type)
            db_sess.commit()
        except Exception:
            return render_template("add_new_type.html", title="Добавление нового типа", form=form,
                                   message='Произошла неизвестная ошибка.')
        finally:
            return redirect('/')  # страницу растраты за месяц
    return render_template("add_new_type.html", title="Добавление нового типа", form=form)


@app.route('/personal_account', methods=['GET'])
@login_required
def personal_account():
    return render_template('personal_account.html', user=current_user)


if __name__ == '__main__':
    db_session.global_init("db/web_db.sqlite")
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
