from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
#---------Bcrypt------------------
bcrypt = Bcrypt(app)

#----------LoginManager-------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.user_login"
login_manager.login_message_category = "success"

app.config['SECRET_KEY'] = 'a72c3251c8451aed32520c20b1ab7475'
#=======DATABASE==============
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#----------App Register----------

from mysite.blog.views import blog
from mysite.auth.views import auth
app.register_blueprint(blog,url_prefix='/blog')
app.register_blueprint(auth,url_prefix='/auth')
