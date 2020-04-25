

# ---------------------------------------------------------------------------- #
#                                    IMPORTS                                   #
# ---------------------------------------------------------------------------- #




# --------------------- Imported the app from the package -------------------- #
from main import app


# ------------------- Imported necessary methods from flask ------------------ #
from flask import render_template, flash, redirect, url_for, request


# ------------------- Imported the password hashing modules ------------------ #
from werkzeug.security import generate_password_hash, check_password_hash


# ---------------------------- Imported the models --------------------------- #
from main.models import User


# ---------------------------- Imported the froms ---------------------------- #
from main.forms import signinform, signupform, updateform, exploreform, exploreform2, exploreform3


#------------------------ imported flask login modules ----------------------- #
from flask_login import login_user, current_user, logout_user, login_required


# ------------------ imported current user from flask login ------------------ #
from flask_login import current_user


# ---------------------- Imported db from init, package ---------------------- #
from main import db

# ------------------------- Imported secrets token and os module for the profile_picture section below  ------------------------------------------------- #

import secrets
import os
from PIL import Image

# ---------------------------------------------------------------------------- #



#login required comes with a link in init file
#login required prevents to gain access if not logged in  --> basically not letting people to access home, about, profile, explore, etc.

#is authenticated prevents to gain access if logged in --> basically not letting people to access signin or singup pages


# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #








# ---------------------------------------------------------------------------- #
#                                    ROUTES                                    #
# ---------------------------------------------------------------------------- #




# ----------------------------- Start Page Route ----------------------------- #
@app.route("/")
@app.route("/start")
def start():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template("start.html", title_given="Start")
    
    
    
# ---------------------------------------------------------------------------- #



# ------------------------------ Home Page Route ----------------------------- #
@app.route("/home")
@login_required
def home():
    
    return render_template("home.html", title_given="Home")
    
    
    
# ---------------------------------------------------------------------------- #



# ----------------------------- About Page Route ----------------------------- #
@app.route("/about")
@login_required
def about():
    return render_template("about.html", title_given="About")
    
    
    
# ---------------------------------------------------------------------------- #



# ---------------------------- Explore Page Route ---------------------------- #
@app.route("/explore" , methods=['GET', 'POST'])
@login_required
def explore():

    

    form1 =  exploreform()
    form2 = exploreform2()
    form3 = exploreform3()
    ans = ''
    qn = ''
    data= []
    searched_user=''
    if form2.validate_on_submit():   
        qn = (str(form2.question2.label.text)).lower()
        ans = (str(form2.question2.data))
        data = User.query.filter_by(branch = ans)
    if form1.validate_on_submit():
        qn = (str(form1.question1.label.text))
        ans = (str(form1.question1.data))
        data = User.query.filter_by(country = ans)
    
    emaill = []
    usernamel = []
    rollnol = []
    branchl=[]
    batchl=[]
    for i in data:
        emaill.append(i.email)
        usernamel.append(i.username)
        rollnol.append(i.rollno)
        branchl.append(i.branch)
        batchl.append(i.batch)

    input_search = str(form3.question3.data)
    searched_user = User.query.filter_by(username = input_search).first()
    image_file = ''
    if searched_user:
        image_file = url_for ('static', filename='pp/' + searched_user.image_file)
        
    return render_template("explore.html", title_given="Explore", email=emaill, username=usernamel, rollno=rollnol, form1=form1, ans=ans, qn=qn , form2=form2, branch= branchl, batch=batchl, form3=form3, searched_user=searched_user, image_file=image_file)



# ---------------------------------------------------------------------------- #



# ---------------------------- General Page Route ---------------------------- #
@app.route("/profile")
@login_required
def profile():
    image_file = url_for ('static', filename='pp/' + current_user.image_file)
    return render_template("profile.html", title_given="General", image_file=image_file)



# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #

# ----------------- making a function for the profile picture ---------------- #
def save_profile_picture(form_profile_picture):
    random_name_part = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_profile_picture.filename)
    randomized_name = random_name_part + f_ext
    profile_picture_path = os.path.join(app.root_path, 'static/pp', randomized_name)


    output_size = (200,200)

    i = Image.open(form_profile_picture)
    i.thumbnail(output_size)




    i.save(profile_picture_path)
    return randomized_name
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
#So what we did here is write a function to provide a location for the image to be saved and also changed the name of the file to a randomized name so that the names never collide and we get no errors even if user upload images with same file name
# random_name_part --> generated by the secrets token ,, 64digit name created
# extension preserved by the os module that helped in seaparating our file name from its extensions
# os again helped in joning the file name providing the directory for them to be saved
# finally we returned the final randomized name so we can call it later on in the route below
# ---------------------------------------------------------------------------- #
#Later i imported PILLOW and resized the images before uploading them just to save space and make things faster
# ---------------------------------------------------------------------------- #




# --------------------- Change Account Details Page Route -------------------- #
@app.route("/security", methods=['GET', 'POST'])
@login_required
def security():
    form = updateform()

    
    if form.validate_on_submit():
        if form.profile_picture.data:
            profile_picture_file = save_profile_picture(form.profile_picture.data)
            current_user.image_file = profile_picture_file

            #if in case profie picture is updated ,, we cretae a instance called profile_picture_file and assign it to the value returned by the function we created above
            # then we assign it to our database by redefining our image_file attribute of our class User in our db model


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



# ---------------------------------------------------------------------------- #



# ---------------------------- Contact Page Route ---------------------------- #
@app.route("/contact")
@login_required
def contact():
    return render_template("contact.html", title_given="Contact")



# ---------------------------------------------------------------------------- #



# ----------------------------- SignIn Page Route ---------------------------- #
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



# ---------------------------------------------------------------------------- #



# ----------------------------- Signup Page Route ---------------------------- #
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



# ---------------------------------------------------------------------------- #



# ---------------------------- Signout Page Route ---------------------------- #
@app.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('start'))

# ---------------------------------------------------------------------------- #
