from flask import Flask, render_template, request, session, url_for, redirect
from models import db, User
from forms import SignupForm, LoginForm
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
db.init_app(app)
app.secret_key = 'development-key'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "GET":
        return render_template('signup.html', form=form)
    elif request.method == "POST":
        if not form.validate():
            return render_template('signup.html', form=form)
        else:
            user = User(form.first_name.data, form.last_name.data,
                        form.email.data, form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
                session['email'] = user.email
                return redirect(url_for('home'))
            except Exception as e:
                return "Something is wrong with the DB: {error}".format(error=e)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', form=form)
    elif request.method == "POST":
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return render_template('login.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
