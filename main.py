from sqlite3.dbapi2 import IntegrityError
from flask import Flask, render_template
from werkzeug.utils import redirect

from data import db_session
import data.db_models
import forms


app = Flask(__name__)
app.config['SECRET_KEY'] = 'check_check_key'


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = data.db_models.User(form.name.data, form.email.data,
                                   form.password.data, form.inn.data)
        try:
            db_sess.add(user)
            db_sess.commit()
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


#def add_new_check():
#    form = forms.AddCheckForm()
#    if form.validate_on_submit():
#        db_sess = db_session.create_session()
#        check = data.db_models.Check(form.str_Qr.data, form.id_type.data,
#                                     form.description.data, form.information.data)
#        db_sess = data.db_session.create_session()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
