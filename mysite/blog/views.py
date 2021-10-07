from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user
from .models import Post
from mysite import db


blog = Blueprint('blog',__name__)

@blog.route("/")
def home():
    post = Post.query.all()
    
    return render_template("Blog/index.html",user=current_user)


#-------------writepost---------------

@blog.route("/write/",methods=['GET','POST'])
@login_required
def write():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash("Title dose not empty","danger")
            return redirect(url_for("blog.write"))
        elif not content:
            flash("Content dose not empty","danger")
            return redirect(url_for("blog.write"))
        else:
            post = Post(title=title,content=content,user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post hase been created","info")
            return redirect(url_for("blog.home"))
    return render_template("Blog/write_post.html")

#----------ReadSinglePost ------------
@blog.route("/read/<int:id>/")
def read_post(id):
    post = Post.query.filter_by(id=id).first()
    return render_template("Blog/read_post.html",post=post)