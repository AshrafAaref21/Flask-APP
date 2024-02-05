from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from companyblog.models import User


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegisterationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    user_name = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='password should match')])
    pass_confirm = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


    def check_email(self, email):
        if User.query.filter_by(email= self.email.data).first():
            raise ValidationError('Your Email has been registered')
        
    def check_username(self, username):
        if User.query.filter_by(user_name= self.username.data).first():
            raise ValidationError('Your User Name has been registered')
        
    

class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    user_name = StringField('User Name', validators=[DataRequired()])
    picture = FileField('Update Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
