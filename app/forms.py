from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import User

#Flask-wtforms is providing data required.

#To attain user inputs for login in HTML
class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

#To gain new users in the registration.html, the the first password input will be compared against the hashed password.
class RegistrationForm(FlaskForm):
    username = StringField(_l('Enter a unique Username'), validators=[DataRequired()])
    email = StringField(_l('Enter a unique email'), validators=[DataRequired(), Email()])  #has email method to ensure is not anytype of input.
    password = PasswordField(_l('Enter a strong Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('PleaseRepeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))

#The function will check if user name exsist in the database by checking Models (User)
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Username taken unfortunately, Please use a different username.'))

#The function will check if email exsist in the database by checking Models (User)
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Email taken unfortunately, Please use a different email address.'))



#Request for Email, this class is temprorarily supressed
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l(' please repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('Change your Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('Tell us something about you'),
                             validators=[Length(min=0, max=1500)])
    submit = SubmitField(_l('Howl yourself'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

#The function will check if user name exsist in the database by checking Models (User)
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

# A button made for submitting Howls
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField(_l('Express some Science today!'), validators=[DataRequired()])
    submit = SubmitField(_l('Howl your findings'))


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=0, max=500)])
    submit = SubmitField(_l('Submit'))

#Will ask details from user to post a jobs/opporunity.
class JobForm(FlaskForm):
    title = StringField(_l('Company Name'), validators =[DataRequired()])
    content = TextAreaField(_l('Requirements'), validators =[Length(min=0, max=1500)])
    submit = SubmitField(_l('Submit'))
