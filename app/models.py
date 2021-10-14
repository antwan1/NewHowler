from datetime import datetime

from flask import json
from app import db
from flask_login import UserMixin
from app import login
from time import time
import jwt
from app import app
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

 # /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# *
# ***************************************************************************************/   

#The Unary Table, full of users. 
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)



# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# *
# ***************************************************************************************/   

#This component of the database model is supposed to retrieve data from registered users, 
#provide hashing for passwords, post user information in the profile section, and use it as a foreign key to retrieve their posts or followers
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    job = db.relationship('Jobpost', backref='author', lazy='dynamic')  #This will also link with jobpost
    about_me = db.Column(db.String(1500)) #Places data about the user here
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        #A self join is a join in which a table is joined with itself (which is also called Unary relationships), 
        # especially when the table has a FOREIGN KEY which references its own PRIMARY KEY.
        'User', secondary=followers,                                                 
        primaryjoin=(followers.c.follower_id == id),                                
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
        # To join a table itself means that each row of the table is combined with itself and with every other row of the table.


    
# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/   
# will return messages sent by the given user.
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')

     #Will return messages received by the given user.   
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    #To be used as an indicator later to refere when was the last time the user has been to the messages tab.
    last_message_read_time = db.Column(db.DateTime)

    
    

# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/   
    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()


# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/   
#Does not work will use this to add to future work
  


   

    #Grabs email from user's gravatar account and compares it to their email to format gravatar pic into profile.
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
   
    
#Must be tested in test.py
#function gathers password from user and creates a hash according to Wekzeug documentation.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

#This checks password with hashed password to log in
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #if user clicks the follow button and they're not following user, they will be appended to the array of followed of the user following.
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
#Removes user from followed list
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
#Counts how many users the current_user is following.
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

#The function that enables post in the home page to display post by followed users through a join. 
    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())




  

#This is not really implemented fully
#This is adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-email-support
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
  #When the user clicks on the emailed link, the token is going to be sent back to the application as part of the URL, and the first thing the view function that handles this URL will do is to verify it. If the signature is valid, then the user can be identified by the ID stored in the payload. Once the user's identity is known, the application can ask for a new password and set it on the user's account.
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            #Since these tokens belong to users, I'm going to write the token generation and verification functions as methods in the User model:
#The get_reset_password_token() function returns a JWT token as a string, which is generated directly by the jwt.encode() function.
            return
        return User.query.get(id)
    def __repr__(self):
        return '<User {}>'.format(self.username)




#Model class for posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __repr__(self):
        return '<Post {}>'.format(self.body)




 
# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/   
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/   
#Tried to make this work by following the tutorial and understand how it can be implemented.
#However it does not work properly and will continue to work on it.



#Model for jobsposting.
class Jobpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
  

   


