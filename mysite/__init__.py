from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

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

#------------Flask-Mail--------------
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT']  = 465
app.config['MAIL_USERNAME'] = 'surajblog47@gmail.com'
app.config['MAIL_PASSWORD'] = '88406439wp'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

#----------App Register----------

from mysite.blog.views import blog
from mysite.auth.views import auth
from mysite.home.views import home

app.register_blueprint(blog,url_prefix='/blog')
app.register_blueprint(auth,url_prefix='/auth')
app.register_blueprint(home,url_prefix='/')
