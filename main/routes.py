from main import app
from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from main.models import User
from main.forms import signinform, signupform, updateform, exploreform, exploreform2

from flask_login import login_user, current_user, logout_user, login_required

from flask_login import current_user

from main import db


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

@app.route("/explore" , methods=['GET', 'POST'])
@login_required
def explore():
    form1 =  exploreform()
    form2 = exploreform2()
    ans = ''
    qn = ''
    data= []
    if form2.validate_on_submit():   
        qn = (str(form2.question2.label.text)).lower()
        ans = (str(form2.question2.data))
        data = User.query.filter_by(branch = ans)
    if form1.validate_on_submit():
        qn = (str(form1.question.label.text)).lower()
        ans = (str(form1.question.data))
        data = User.query.filter_by(country = ans)
    
    emaill = []
    usernamel = []
    rollnol = []
    imagel=[]
    branchl=[]
    for i in data:
        emaill.append(i.email)
        usernamel.append(i.username)
        rollnol.append(i.rollno)
        imagel.append(i.image_file)
        branchl.append(i.branch)

    
        
    return render_template("explore.html", title_given="Explore", email=emaill, username=usernamel, rollno=rollnol, image_file=imagel, form1=form1, ans=ans, qn=qn , form2=form2, branch= branchl)









@app.route("/profile")
@login_required
def profile():
    image_file = url_for ('static', filename='pp/' + current_user.image_file)
    return render_template("profile.html", title_given="General", image_file=image_file)










@app.route("/security", methods=['GET', 'POST'])
@login_required
def security():
    form = updateform()

    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.fname = form.fname.data
        current_user.mname = form.mname.data
        current_user.lname = form.lname.data
        current_user.degree = form.degree.data
        current_user.branch = form.branch.data
        current_user.rollno = form.rollno.data
        current_user.social = form.social.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash('Your Account Has Been Updated', 'success text-center')
        return redirect(url_for('profile'))

#i dont think i neeed to keep explaining this, flask login is the best thing out there
#had to import db

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.fname.data = current_user.fname
        form.mname.data = current_user.mname
        form.lname.data = current_user.lname
        form.degree.data = current_user.degree
        form.branch.data = current_user.branch
        form.rollno.data = current_user.rollno
        form.social.data = current_user.social
        form.gender.data = current_user.gender
#this just helps to autofill the data in the form incase we dont fill it 
        
    
    
        

    return render_template("security.html", title_given="Security", form=form)
    






















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

