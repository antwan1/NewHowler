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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


# /***************************************************************************************
# *    Title: Mega Flask Tutorial
# *    Author: Miguel Grinberg
# *    Date: 01/10/2021
# *    Code version: 2.0
# *    Availability:https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
# *
# ***************************************************************************************/

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


