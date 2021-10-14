from flask import render_template
from app import app, db


# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
# *
# ***************************************************************************************/

@app.errorhandler(404)# This is to declare to flask that this is a custom error handler.
#This will be called automatically instead of the default errors.
def not_found_error(error):
    #404 is when item/object is not found in the database.
    return render_template('404.html'), 404


# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
# *
# ***************************************************************************************/

@app.errorhandler(500) # This is to declare to flask that this is a custom error handler.
#This will be called automatically instead of the default errors
def internal_error(error):
    #error 500 is whenever is when there is something wrong with the server (internally).
    db.session.rollback()
    #To ensure it doesn't interfere with the database, a rollback is issued through the database terminal.
    return render_template('500.html'), 500


