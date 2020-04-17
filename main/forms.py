from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, Form, RadioField, SelectField, ValidationError, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField
from main.models import User

from flask_login import current_user
#This is done for the updateform



class signinform(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Sign In')




class signupform(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])

    mname = StringField('Middle Name')

    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])

    degree = StringField('Degree', validators=[DataRequired(), Length(min=2, max=20)])

    branch = StringField('Branch', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    batch = StringField('Batch Of', validators=[DataRequired(), Length(min=9, max=9)])

    rollno = StringField('Roll No', validators=[DataRequired(), Length(min=5)])
    


    birthdate = DateField("Date of Birth", format='%Y-%m-%d', validators=[DataRequired()])

    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=20)])

    social = TextAreaField(' How can we reach you ')

    password = PasswordField('Password', validators=[DataRequired()])



    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    
    

    recaptcha = RecaptchaField()


    

    gender = RadioField('Gender', choices= [('Male', 'Male'), ('Female', 'Female'), ('LGBTQ...', 'Amongst LGBTQ.....')])


    age = SelectField("Age group", choices=[
        ('1', '0-10'), ('2', '10-25'), ('3', '35-60'), ('4', '50+')
    ])


    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username already exists.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email already exists.')
    def validate_rollno(self, rollno):
        user = User.query.filter_by(rollno=rollno.data).first()
        if user:
            raise ValidationError('The Roll No already exists.')









#we imported current user so that:
#incase someone wants to update without some changes to their stuff
#the validators below will show error because those unchnaged values exist in our database and wont let us submit
#hence we import curnt user and apply conditions that the conditional work only if different calues are input
class updateform(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])

    mname = StringField('Middle Name')

    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])

    degree = StringField('Degree', validators=[DataRequired(), Length(min=2, max=20)])

    branch = StringField('Branch', validators=[DataRequired(), Length(min=2, max=20)])


    rollno = StringField('Roll No', validators=[DataRequired(), Length(min=5)])
    



    social = TextAreaField(' How can we reach you ')


    gender = RadioField('Gender', choices= [('Male', 'Male'), ('Female', 'Female'), ('LGBTQ...', 'Amongst LGBTQ.....')])




    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username already exists.')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email already exists.')
    def validate_rollno(self, rollno):
        if rollno.data != current_user.rollno:
            user = User.query.filter_by(rollno=rollno.data).first()
            if user:
                raise ValidationError('The Roll No already exists.')
#added  if rollno.data != current_user.rollno: these in our validator functions so that we can submit our own preexisting values






class exploreform(FlaskForm):
    question = StringField('Country', validators=[DataRequired()])

    submit = SubmitField('Search')

class exploreform2(FlaskForm):
    question2 = StringField('Branch', validators=[DataRequired()])

    submit2 = SubmitField('Search')

    