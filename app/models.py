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


#This will load the user consistently
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

 # /***************************************************************************************
            ##LEARNED FROM##
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
        ##LEARNED FROM##
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
    #Index the user's ID and ensure each user is unique.
    username = db.Column(db.String(64), index=True, unique=True)
    #User name is unique to reduce redundances 
    email = db.Column(db.String(120), index=True, unique=True)
    #Emails are unique for the same reason as emails
    password_hash = db.Column(db.String(128))
    #Converted password of the user stored and indexed with the user.
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    #To track the posts through the author's user id. 
    job = db.relationship('Jobpost', backref='author', lazy='dynamic')  
    #This relates the job post back to the author same as user.
    about_me = db.Column(db.String(1500)) #Places data about the user here
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    #Capture's the data from the view to indicate when user was last online.
    followed = db.relationship(
        #A self join is a join in which a table is joined with itself (which is also called Unary relationships), 
        # especially when the table has a FOREIGN KEY which references its own PRIMARY KEY.
        'User', secondary=followers,                                                 
        primaryjoin=(followers.c.follower_id == id),                                
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
        # To join a table itself means that each row of the table is combined with itself and with every other row of the table.


    
# /***************************************************************************************
            ##LEARNED FROM##
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
            ##LEARNED FROM##
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/   
    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        #To indicate when the user was last seen in the messages tab.
        return Message.query.filter_by(recipient=self).filter(
            #Counts messages from last time read.
            Message.timestamp > last_read_time).count()


# /***************************************************************************************
                ##LEARNED FROM##
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



# /***************************************************************************************
            ##LEARNED FROM##
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/   
    #if user clicks the follow button and they're not following user, they will be appended to the array of followed of the user following.
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

# /***************************************************************************************
            ##LEARNED FROM##
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/   
#Removes user from followed list
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)



# /***************************************************************************************
                ##LEARNED FROM##
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/   
#Counts how many users the current_user is following.

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0


# /***************************************************************************************
            ##LEARNED FROM##
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/   

#The function that enables post in the home page to display post by followed users through a join. 
    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())




  






#Model class for posts
class Post(db.Model):
    #Indexes all posts in the database.
    id = db.Column(db.Integer, primary_key=True)
    #The content stored.
    body = db.Column(db.String(500))
    #Timestamp is used to order the posts in a descending order.
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #Relates back to the author. 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __repr__(self):
        return '<Post {}>'.format(self.body)




 
# /***************************************************************************************
                ##LEARNED FROM##
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
            ##LEARNED FROM##
# *    Title: Flask Tutorial 
# *    Author: Corey Schaffer
# *    Date: 07/10/2021
# *    Code version: N/A
# *    Availability:https://www.youtube.com/watch?v=u0oDDZrDz9U&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=8
# *
# ***************************************************************************************/           


#Model for jobsposting.
class Jobpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



  

   


