from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,validators,SubmitField,FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired,Length,Email,ValidationError
from wtforms.fields.html5 import EmailField
from flask_login import current_user
from .models import User



class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    register = SubmitField('Register')
    
class LoginForm(FlaskForm):
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    
    login = SubmitField('Login')

class AccountUpdateForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    picture = FileField("Profile Picture", validators=[FileAllowed(['jpg','png'])])
    update = SubmitField('Update')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("That email is already taken please try different email!")