from mysite import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=False,nullable=False)
    email = db.Column(db.String(25),unique=True,nullable=False)
    password = db.Column(db.String(20),unique=False,nullable=False)
    image_file = db.Column(db.String(50),nullable=False,default="default.png")
    posts = db.relationship('Post',backref='author',lazy=True)
    def __repr__(self):
        return f"{self.name},{self.email},{self.password},{self.pic_file}"
        
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),     nullable=False)
    content = db.Column(db.Text,nullable=False)
    post_created = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    
    def __repr__(self):
        return f"{self.title},{self.content},{self.post_created},{self.user_id}"