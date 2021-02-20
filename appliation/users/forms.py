from flask_wtf import FlaskForm
from application.Model import User
from wtforms.fields.simple import TextAreaField
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms.fields import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,Length,ValidationError


class RegistrationForm(FlaskForm):
    userName = StringField(' Name :',
                                validators=[DataRequired(), Length(min=3,max=50,message= u'Name characters between 3 and 50')])

    email = StringField("Email :",validators=[DataRequired(),
                                                 Email(message=u'its not a valid email address')])
    password = PasswordField("Password :",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password :",validators=[DataRequired(),
                                                                      EqualTo('password',message="Passwords do not match")])
    picture = FileField("Upload Image :",validators=[FileRequired(),FileAllowed(['jpg','png'],'Images only')])
    # reCaptcha = RecaptchaField()
    submit = SubmitField("Sign Up")

#     Custom Validator for Email
    def validate_email(self,email):
        user = User.query.filter_by(user_email=email.data).first()
        if user:
            raise ValidationError("That user has already been taken")

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    rememberMe = BooleanField("RememberMe")
    submit = SubmitField("Login")

class RequestForm(FlaskForm):
    email = StringField("Email :", validators=[DataRequired(),
                                               Email(message=u'its not a valid email address')])
    submit = SubmitField("Request Reset")
    def validate_email(self,email):
        user = User.query.filter_by(user_email=email.data).first()
        if user is None:
            raise ValidationError("There is no user with this email")
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password :", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password :", validators=[DataRequired(),
                                                                       EqualTo('password',message="Passwords do not match")])
    submit = SubmitField('Reset Password')

class ProfileForm(FlaskForm):
    userName = StringField(' Name :',
                                validators=[DataRequired(), Length(min=3,max=50,message= u'Name characters between 3 and 50')])

    email = StringField("Email :", validators=[DataRequired(),
                                                 Email(message=u'its not a valid email address')])
    picture = FileField("Upload Image :", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only')])
    comment = TextAreaField('Comment :')
    # reCaptcha = RecaptchaField()
    submit = SubmitField("Update Profile")
