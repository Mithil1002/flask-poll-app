from poll import db
from poll import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)


class User(UserMixin, db.Model):
    # id = db.Column(db.Integer(), primary_key=True)
    email_address = db.Column(db.String(length=30), nullable=False, unique=True)
    username = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=200), nullable=False)
    polls = db.relationship('Poll', backref='owned_user', lazy=True)


class Poll(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(350))
    option_one = db.Column(db.String(100))
    option_two = db.Column(db.String(100))
    option_three = db.Column(db.String(100))
    option_four = db.Column(db.String(100))
    one_count = db.Column(db.Integer, default=0)
    two_count = db.Column(db.Integer, default=0)
    three_count = db.Column(db.Integer, default=0)
    four_count = db.Column(db.Integer, default=0)
    total_count = db.Column(db.Integer, default=0)
    owner = db.Column(db.String(50), db.ForeignKey('user.username'))

    def total(self):
        return self.one_count + self.two_count + self.three_count + self.four_count
