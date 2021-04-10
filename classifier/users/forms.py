from flask_wtf import FlaskForm

from wtforms import SubmitField, SelectField, TextAreaField, PasswordField, StringField, BooleanField, IntegerField, RadioField
from wtforms.validators import DataRequired, InputRequired, Length, Email,EqualTo, ValidationError
from classifier.models import User, Image
from wtforms.fields.html5 import EmailField

class RegistrationForm(FlaskForm):
    email = EmailField("Email", validators=[Email(), DataRequired()])
    qualifications = TextAreaField("Please briefly detail your qualifications as a bird identifier?",
                                   validators=[DataRequired()])
    expertise = RadioField("What is Your Level of Expertise",
                           choices=[("1","Enthusiast"), ("2","Long time Birder"), ("3","Expert Birder"),
                                    ("4","Professionally recognized Birder")], validators=[DataRequired()])
    submit = SubmitField("Register")


    def validate_email(self, email):
        """
        pre-check that email is unique
        :param field: email field from submitted form
        :return:
        """
        user = User.query.filter(User.email == email.data).first()

        if user:
            raise ValidationError("That email is already registered, Log In")



class RegistrationFormEdit(FlaskForm):
    email = EmailField("Email", validators=[Email(), DataRequired()])
    qualifications = TextAreaField("Please briefly detail your qualifcations as a bird identifier?",
                                   validators=[DataRequired()])
    password = PasswordField("Password", validators=[])
    expertise = RadioField("What is Your Level of Expertise",
                           choices=[("1","Enthusiast"), ("2","Long time Birder"), ("3","Expert Birder"),
                                    ("4","Professionally recognized Birder")], validators=[DataRequired()])
    submit = SubmitField("Register")


class LogInForm(FlaskForm):
    email = EmailField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("LogIn")
