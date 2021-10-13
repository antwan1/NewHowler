
from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, g, current_app, abort
from flask_login import login_user, logout_user, current_user, login_required

from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from wtforms import form
from app import app, db
from app.forms import JobForm, LoginForm, MessageForm, RegistrationForm, EditProfileForm, \
    EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import Jobpost, Message, Notification, User, Post
from app.email import send_password_reset_email
from flask import g
from flask_babel import get_locale
from langdetect import detect, LangDetectException
from flask import jsonify

import feedparser








   

@app.before_request  #Checks if user is logged to know when they have been last seen.
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 20/08/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination
# *
# ***************************************************************************************/

@app.route('/')
@app.route('/homepage', methods=['GET', 'POST'])  #This will direct the user to the home page.
@login_required
def home():
    form = PostForm()
         
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)  
        #Once form is submitted, it will be added to the database.
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('home'))
    page = request.args.get('page', 1, type=int)
    #pagination is adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('home', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('home', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('home.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

# Redirects user to jobs landing page, (might not be implemented).
@app.route("/opportunities" ,  methods=['GET', 'POST'])
@login_required
def opportunity():
    page = request.args.get('page', 1, type=int)
    posts = Jobpost.query.order_by(Jobpost.date_posted.desc()).paginate(
        #pagination is adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination
        page, app.config['POSTS_PER_PAGE'], False) #Sets the amount of post to placed from config.py
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('oppor.html' , title=_('create job'), posts=posts.items, next_url=next_url,
                           prev_url=prev_url)
#If user clicks on 'Explore', Html will render followed post from current users.


# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 20/08/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination
# *
# ***************************************************************************************/
@app.route('/explore')
@login_required
def explore():
    #
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        
        
        page, app.config['POSTS_PER_PAGE'], False) #Sets the amount of post to placed from config.py
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('home.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)







# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 02/08/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
# *
# ***************************************************************************************/
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Access to log in page, however if there is a current user from the db is already logged, then it redirects to home
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    #If user is logged in, it redirects them to the home page.
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #Username is validated if it exists in the database.
        if user is None or not user.check_password(form.password.data):
            #However if there use doesn't exist in the database
            # Or the password is incorrect, it will flash a message
            flash(_('Invalid username or password'))  
            return redirect(url_for('login'))  
        login_user(user, remember=form.remember_me.data)
        #If user desired access to another page before logging in,
        #After logging in, it will redirect the user to the previous page clicked.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            #Otherwise it will make the user go to the home page
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title=_('Sign In'), form=form)

#To log out user by using logging library
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 02/08/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
# *
# ***************************************************************************************/

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #Once validation from forms is completed and validated
        user = User(username=form.username.data, email=form.email.data)
        #Data will be implemented into the user database
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        #Uses Bootstrap libary to indicate success
        flash(_('Congratulations, you are now a registered user!'))
        #Then return the user back to the login page, to log them back in
        return redirect(url_for('login'))
    return render_template('register.html', title=_('Register'), form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title=_('Reset Password'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)



# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 15/09/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars
# *
# ***************************************************************************************/

@app.route('/user/<username>')
@login_required
def user(username):
    #This will search to see if the user exsist or get a 404 custom error message
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
#Paginate all of the current users posts in order
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False) 
    #This should only display 10 post per page according to config, if theres most than 10, then it will paginate
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    #if theres nop previous post, it will render back to the user's profile page.
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)



# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 15/09/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars
# *
# ***************************************************************************************/



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        #Which ever input is added to the form, will become the new username and personal information.
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        #This only flashes if WTForms believes it is successful.
        flash(_('Your inputs have been updated'))
        return redirect(url_for('edit_profile'))
    #Otherwise it will return the previous inputs if validation has an error
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)





# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 23/09/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers
# *
# ***************************************************************************************/
@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            #if user doesn't exsist when pressing follow
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('home'))
        if user == current_user:
            #This shouldn't happen, however if it occurs then the current user can't follow their selves.
            flash(_('You cannot follow yourself!'))
            return redirect(url_for('user', username=username))
        #if validate_on_submit then the user following will be appended to a list of followers.
        current_user.follow(user)
        db.session.commit()
        flash(_('You are following %(username)s!', username=username))
        #This will flash a message for success
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('home'))



# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 23/09/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers
# *
# ***************************************************************************************/
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('home'))
        if user == current_user:
            #This shouldn't happen again, however this prevents a bug.
            flash(_('You cannot unfollow yourself!'))
            return redirect(url_for('user', username=username))
        #if user unfollows, they will be removed from the current followers list of that specific user.
        current_user.unfollow(user)
        db.session.commit()
        flash(_('You are not following %(username)s.', username=username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('home'))

# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/

@app.route('/messages')
@login_required
def messages():
    #Last time the user saw went to the messages tab
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            #This will paginate the messages
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)




#Renders the about us on from the footer
@app.route('/about')
def about():
    return render_template('about.html')

#Renders FAQ questions from the footer
@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')



@app.before_request
def before_request():
    
    g.locale = str(get_locale())



# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
# *
# ***************************************************************************************/

@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)





@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@app.route('/job/new', methods=['GET', 'POST'])
@login_required
def new_jobs():
    form = JobForm()
    if form.validate_on_submit():
        
        post = Jobpost(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        #Once form is submitted, it will be added to the database.
        flash('your job post has been created', 'success')
        return redirect(url_for('opportunity'))
    return render_template('createjob.html' , title=_('create job'), form=form, legend = 'Job Creation')

@app.route('/job/<int:job_id>')
def job (job_id):
    post =Jobpost.query.get_or_404(job_id)  #Gets the id of the post clicked.
    return render_template('job.html', title=post.title, post=post)



app.route('/job/<int:job_id>/update', methods=['GET', 'POST'])
@login_required
def update_job (job_id):
    post =Jobpost.query.get_or_404(job_id)
    if post.author != current_user:
         abort(403)  #Http response for forbidden status code
    form = JobForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data  #if form is valid, jobpost will update
        db.session.commit()  
        flash('youre post has been updated!')   
        return redirect(url_for('job', job_id = post.id ))  
    elif request.method == 'GET':                               
        form.title.data = post.title
        form.content.data = post.content
    return render_template('createjob.html', title=_('Update Job'), 
            form=form, legend = 'Update Post' )

@app.route("/post/<int:job_id>/delete", methods=['POST'])
@login_required
def delete_job(post_id):
    post = Jobpost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('home'))

# BBC_FEED = "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml"

 #Place holder free RSS feeds, should be replaced with scientific news 

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml', 
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}




@app.route("/news", methods=['GET', 'POST'])
@login_required
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
                publication = "bbc"
    else:
                publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])

    return render_template("news.html",articles=feed['entries'])



