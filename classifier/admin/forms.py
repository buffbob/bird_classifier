from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, IntegerField, RadioField
from wtforms.validators import InputRequired


class ClassifyForm(FlaskForm):
    is_male = RadioField("Choose Sex", choices=[("1", "Male"), ("0","Female"), ("-1", "unsure")], validators=[InputRequired()])
    is_juvenile = RadioField("Is this a juvenile", choices=[("0", "No"), ("1","Yes"),("-1","unsure")], validators=[InputRequired()])
    is_standard = RadioField("Is this a standard?", choices=[("0", "No"),("1", "Yes")], validators=[InputRequired()])
    quality = RadioField("Image Quality", choices=[("1","Acceptable"),("2","Good"),("3","Perfect")], validators=[InputRequired()])
    certainty = RadioField("Your Certainty", choices=[("1","Probably"), ("2", "Yup"), ("3","Bet my Life")], validators=[InputRequired()])
    birdname = StringField('birdname')
    count = IntegerField('count')
    image_id = IntegerField("image_id")
    image_folder = StringField("image_folder")
    submit = SubmitField("Classify")


class ClassifyForm2(FlaskForm):
    is_male = SelectField("Choose Sex", choices=[("1", "Male"), ("0","Female"), ("-1", "unsure")], validators=[InputRequired()])
    is_juvenile = SelectField("Is this a juvenile", choices=[("0", "No"), ("1","Yes"),("-1","unsure")], validators=[InputRequired()])
    is_standard = SelectField("Is this a standard?", choices=[("0", "No"),("1", "Yes")], validators=[InputRequired()])
    quality = SelectField("Image Quality", choices=[("1","Acceptable"),("2","Good"),("3","Perfect")], validators=[InputRequired()])
    certainty = SelectField("Your Certainty", choices=[("1","Probably"), ("2", "Yup"), ("3","Bet my Life")], validators=[InputRequired()])
    birdname = StringField('birdname')
    count = IntegerField('count')
    image_id = IntegerField("image_id")
    image_folder = StringField("image_folder")
    submit = SubmitField("Classify")
