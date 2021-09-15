from flask import Blueprint,render_template,request,flash,redirect,url_for
from mysite import bcrypt,db
from .forms import LoginForm, RegistrationForm,AccountUpdateForm
from .models import User
from flask_login import login_required,login_user,current_user,logout_user
from .utils import image_save

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
            return redirect(url_for("auth.home"))
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
@login_required       
@auth.route("/home",methods=['GET','POST'])
def home():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            print(form.picture.data)
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
