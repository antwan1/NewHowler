import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Dont guess please'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    POSTS_PER_PAGE = 30 #This will be a config for pagination, this can be changed to slow down mass information if required.

    #To emulate mail server, remember to use:  python -m smtpd -n -c DebuggingServer localhost:8025
    LANGUAGES = ['en', 'es']  #Supported languages for the website.
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY') #Microsoft Azure Transaltion Api

    