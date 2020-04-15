from main import app
from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from main.models import User
from main.forms import signinform, signupform
from main import db

from flask_login import login_user, current_user, logout_user, login_required

#login required comes with a link in init file
#login required prevents to gain access if not logged in 

#is authenticated prevents to gain access if logged in --> basically not letting people to access signin or singup pages


@app.route("/")
@app.route("/start")
def start():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template("start.html", title_given="Start")

@app.route("/home")
@login_required
def home():
    return render_template("home.html", title_given="Home")

@app.route("/about")
@login_required
def about():
    return render_template("about.html", title_given="About")



@app.route("/contact")
@login_required
def contact():
    return render_template("contact.html", title_given="Contact")

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = signinform()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                return redirect(url_for('home'))
            else:
                flash ('Invalid Email Address or Password', 'danger')
        else:
                flash ('Invalid Email Address or Password', 'danger')

    return render_template("signin.html", title_given="Sign In", form=form)




@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = signupform()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, birthdate = form.birthdate.data, age = form.age.data, gender = form.gender.data, fname = form.fname.data, mname = form.mname.data, lname=form.lname.data, batch = form.batch.data, degree=form.degree.data, branch=form.branch.data, rollno=form.rollno.data, country=form.country.data,social=form.social.data)
        db.session.add(new_user)
        db.session.commit()
        flash('New user created', 'success')
        return redirect(url_for('signin'))

        
    return render_template("signup.html", title_given="Sign Up", form=form)

@app.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('start'))

