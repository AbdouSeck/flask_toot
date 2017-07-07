from flask import Flask, render_template, request, session, url_for, redirect
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
db.init_app(app)
app.secret_key = 'development-key'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/home', methods=['POST', 'GET'])
def home():
    if 'email' in session:
        form = AddressForm()
        places = []
        my_coordinates = (42.360091, -71.094160)
        if request.method == 'POST':
            if not form.validate():
                render_template('home.html', form=form)
            else:
                address = form.address.data
                p = Place()
                my_coordinates = p.address_to_latlng(address)
                places = p.query(address)
                return render_template('home.html', form=form,
                                       my_coordinates=my_coordinates,
                                       places=places)
        elif request.method == 'GET':
            return render_template('home.html',
                                   form=form,
                                   my_coordinates=my_coordinates,
                                   places=places)
    else:
        return redirect(url_for('login'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))
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
    if 'email' in session:
        return redirect(url_for('home'))
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


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
