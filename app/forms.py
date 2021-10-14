from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.fields.simple import FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import User
from flask_wtf.file import FileField, FileAllowed

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
        _l('Please Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))




# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 02/08/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
# *
# ***************************************************************************************/
#The function will check if user name exsist in the database by checking Models (User)
    def validate_username(self, username):
        #Query through user model for the first result of username equaling to the input of the of user. 
        user = User.query.filter_by(username=username.data).first()
        #if user doesn't exist, then it will raise a validation error.'
        if user is not None:
            raise ValidationError(_('Username taken unfortunately, Please use a different username.'))



# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 02/08/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
# *
# ***************************************************************************************/
#The function will check if email exsist in the database by checking Models (User)
    def validate_email(self, email):
        #Query through user model for the first result of emails equaling to the input of the of user. 
        user = User.query.filter_by(email=email.data).first()
        #if email data doesn't exist', then it will raise a validation error
        if user is not None:
            raise ValidationError(_('Email taken unfortunately, Please use a different email address.'))





#Request for Email, this class is temprorarily supressed for testing
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))

#A form when the user receives a reset password request.
class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l(' please repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))

#A form to enable users to change their status and Identity.
class EditProfileForm(FlaskForm):
    username = StringField(_l('Change your Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('Tell us something about you'),
                             validators=[Length(min=0, max=1500)])
    submit = SubmitField(_l('Howl yourself'))

# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 10/08/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
# *
# ***************************************************************************************/

    def __init__(self, original_username, *args, **kwargs):
        #creates an overloaded constructor that accepts the original_username as an argument.
        super(EditProfileForm, self).__init__(*args, **kwargs)
        #The username is saved as instance variable
        self.original_username = original_username

#The function will check if user name exsist in the database by checking Models (User)
    def validate_username(self, username):
        #The orginal user name is checked to create any duplicates.
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

# A button made for submitting Howls
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

#A form for submitting Posts in Homepage
class PostForm(FlaskForm):
    post = TextAreaField(_l('Express some Science today!'), validators=[DataRequired()])
    submit = SubmitField(_l('Howl your findings'))

#A form for submitting Private Messages
class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=0, max=500)])
    submit = SubmitField(_l('Submit'))

#Will ask details from user to post a jobs/opporunity.
class JobForm(FlaskForm):
    title = StringField(_l('Company Name'), validators =[DataRequired()])
    content = TextAreaField(_l('Requirements'), validators =[Length(min=0, max=1500)])
    submit = SubmitField(_l('Submit'))


class ApplicationForm(FlaskForm):
    name = StringField(_l(' Name of Applicant'), validators = [DataRequired()])
    last_name = StringField(_l('Last name of Applicant'), validators=[DataRequired()])
    phone_number = StringField(_l('Phone Number'), validators=[DataRequired()])
    cv = FileField('Update Profile Picture', validators=[FileAllowed(['pdf', 'doc'])])