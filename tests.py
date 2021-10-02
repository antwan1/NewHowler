from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self): # instance method to set initial state before each test method is run.


        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self): #Python Unit test documentation = instance method to perform cleanup after each test method completes.
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self): #To Test password_hash from config
        u = User(username='molinaa')
        u.set_password('1234')
        self.assertFalse(u.check_password('watermelon'))
        self.assertTrue(u.check_password('1234'))


#This is an example placed by corey schafer on youtube
    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'  #if need to test on own profile pic,
                                                                               # use 'https://www.gravatar.com/avatar/f6fdc1d3c21b4b1fedb1958d6370d49c' with antoniore385@gmail.com     
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))


#Add users to test follow
    def test_follow(self):
        u1 = User(username='antonio', email='antonio@example.com')
        u2 = User(username='palla', email='palla@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

#To test emails.
# with mail.record_messages() as outbox:

#     mail.send_message(subject='testing',
#                       body='test',
#                       recipients=emails)

#     assert len(outbox) == 1
#     assert outbox[0].subject == "testing"
#Antonio should follow palla
        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'palla')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'antonio')
#Antonio should unfollow palla
        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='antonio', email='antonio@example.com')
        u2 = User(username='palla', email='palla@example.com')
        u3 = User(username='lisa', email='lisa@example.com')
        u4 = User(username='luke', email='luke@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from antonio", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from palla", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from lisa", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from luke", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # antonio follows palla
        u1.follow(u4)  # antonio follows luke
        u2.follow(u3)  # palla follows lisa
        u3.follow(u4)  # lisa follows luke
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])
#f1 is not appending the right followers. 
if __name__ == '__main__':
    unittest.main(verbosity=2)