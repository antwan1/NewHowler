import os

basedir = os.path.abspath(os.path.dirname(__file__))

#When the app is initialized, the variables in config.py are used to configure Flask and its extensions are accessible via the app. 
# config dictionary – e.g. app. config["DEBUG"] .
#
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Dont guess please'   #Token key to protect against malicious users who do cookie tampering.
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')  
    SQLALCHEMY_TRACK_MODIFICATIONS = True  #So I can track modifications from the database
    #To emulate mail server, remember to use:  python -m smtpd -n -c DebuggingServer localhost:802
    #Check Flask-Mail for documentation
 
    ADMINS = ['antoniore385@gmail.com']
    POSTS_PER_PAGE = 10 #This will be a config for pagination, this can be changed to slow down mass information if required.

    

    