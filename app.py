from app.models import Message, Post, User
from app import app, db,cli



if __name__ == '__main__':
    app.run(debug=True)
