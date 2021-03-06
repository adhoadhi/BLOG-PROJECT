from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    blogs = db.relationship('Blog', backref='users', lazy="dynamic")
    comments = db.relationship("Comment", backref="user", lazy="dynamic")


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.username}'



class Blog(db.Model):

    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(300), index=True)
    content = db.Column(db.String(300), index=True)
    category = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    

    comments = db.relationship('Comment', backref='blog', lazy="dynamic")

    date = db.Column(db.String)
    time = db.Column(db.String)

    def save_blog(self, blog):
        ''' Save the blogs '''
        db.session.add(blog)
        db.session.commit()

    # display blogs
    @classmethod
    def get_blogs(id):
        blogs = Blog.query.filter_by(category = id).all()
        return blog

    def __repr__(self):
        return f"Blog('{self.id}', '{self.time}')"



class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_comment = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    date = db.Column(db.String)
    time = db.Column(db.String)

    def save_comment(self):
        ''' Save the comments '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(blog_id=id).all()
        return comments