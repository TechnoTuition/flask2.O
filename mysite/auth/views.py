from flask import Blueprint,render_template,request,flash,redirect,url_for
from mysite import bcrypt,db,mail
from .forms import LoginForm, RegistrationForm,AccountUpdateForm,RequestResetForm,ResetPassword
from .models import User

#get_reset_token,verify_reset_token
from flask_login import login_required,login_user,current_user,logout_user
from .utils import image_save,send_reset_email
from flask_mail import Message
from mysite.home.views import home

from mysite.blog.models import Post

auth = Blueprint('auth',__name__)

#1--------login system----------------

@auth.route("/login/",methods=['GET','POST'])
def user_login():
    if current_user.is_authenticated:
            flash("You have already Logged in","danger")
            return redirect(url_for("auth.home"))
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=True)
            flash("You are Successfully logged in","success")
            return redirect("/")
        else:
            flash("email or password dose not match ","danger")
            return redirect(url_for("auth.user_login"))
    return render_template("auth/login.html",title="Login",form=form)


#----------signup--------------------

@auth.route("/signup/",methods=['GET','POST'])
def user_signup():
    if current_user.is_authenticated:
            flash("You have already Logged in","danger")
            return redirect(url_for("auth.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("Email Account Already Exist","danger")
            return redirect(url_for("auth.user_login"))
        else:
            pass_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            new_user = User(name=form.username.data,email=form.email.data,password=pass_hash)
            db.session.add(new_user)
            db.session.commit()
            flash("Account hase been created ","success")
            return redirect(url_for("auth.user_login"))
    return render_template("auth/signup.html",title="Signup", form=form)
    
#-----------------logout--------------

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are Successfully Logout ","success")
    return redirect(url_for("auth.user_login"))

#--------------accountinfo------------    
@auth.route("/home",methods=['GET','POST'])
@login_required
def home():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_data = image_save(form.picture.data)
            current_user.image_file = picture_data
        current_user.name = form.username.data
        current_user.email = form.email.data
        db.session.commit()
    
    elif request.method == "GET":
            form.username.data = current_user.name
            form.email.data = current_user.email

    image_file = url_for('static',filename= f'profile_pics/{current_user.image_file}')
    return render_template("auth/home.html",user=current_user,image_file=image_file,form=form)

#----------Account Delete-------------

@login_required
@auth.route("delete/<int:id>",methods=['GET','POST'])
def delete(id):
    
    if request.method == "POST":
        user = User.query.filter_by(id=id).first()
        db.session.delete(user) 
        db.session.commit()
        logout_user()
        flash("your account hase been deleted ","success")
        return redirect(url_for("auth.user_signup"))
    return redirect(url_for("auth.user_signup"))

#----------RequestReset-------------


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Hello",           sender="surajblog47@gmail.com",
                  recipients=[user.email])
    msg.body = f"""To reset your password,visit the following link:
        {url_for('auth.new_password',token=token,_external=True)}"""
    mail.send(msg)

@auth.route("/reset",methods=['GET','POST'])
def request_reset():
    if current_user.is_authenticated:
            flash("You have already Logged in","danger")
            return redirect(url_for("auth.home"))
    form = RequestResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("email dose not exist ","info")
            return redirect(url_for("auth.request_reset"))
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.","info")
        return redirect(url_for("auth.user_login"))
    return render_template("auth/request_reset.html",form=form)

#--------------New Password----------

@auth.route("/newpass/<token>",methods=['GET','POST'])
def new_password(token):
    if current_user.is_authenticated:
            flash("You have already Logged in","danger")
            return redirect(url_for("auth.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid token or expired token")
        return redirect(url_for("auth.request_pass"))
    form = ResetPassword()
    if form.validate_on_submit():
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = pass_hash
        db.session.commit()
        flash("Your Password has been Updated!","success")
        return redirect(url_for("auth.user_login"))
    return render_template("auth/newpass.html",form=form)
    
   