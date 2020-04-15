from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, Form, RadioField, SelectField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField
from main.models import User



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

    social = StringField(' How can we reach you ')

    password = PasswordField('Password', validators=[DataRequired()])



    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    
    

    recaptcha = RecaptchaField()


    

    gender = RadioField('Gender', choices= [('1', 'Male'), ('2', 'Female'), ('3', 'Amongst LGBTQ.....')])


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
