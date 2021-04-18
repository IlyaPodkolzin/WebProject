from flask import Flask, render_template
from data import db_session
import forms


app = Flask(__name__)
app.config['SECRET_KEY'] = 'check_check_key'


@app.route('/')
@app.route('/registration')
def registration():
    form = forms.RegistrationForm()
    return render_template('registration.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
