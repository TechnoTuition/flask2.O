import secrets
import os
from mysite import app,mail
from PIL import Image
from flask_mail import Message
from flask import url_for


def image_save(form_picture):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_picture.filename)
    pic_fn = random_hex + f_ext
    
    picture_path = os.path.join(app.root_path,'static/profile_pics',pic_fn)
    
    i = Image.open(form_picture)
    size = (124,124)
    i.thumbnail(size)
    i.save(picture_path)
    return pic_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Hello",           sender="noreply@demo.com",
                  recipients=[user.email])
    msg.body = """To reset your password,visit the following link:
        {url_for('new_password',token=token,_external=True)}"""
    mail.send(msg)