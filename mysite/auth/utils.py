import secrets
import os
from mysite import app
from PIL import Image

def image_save(form_picture):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_picture.filename)
    pic_fn = random_hex + f_ext
    
    picture_path = os.path.join(app.root_path,'static/profile_pics',pic_fn)
    
    i = Image.open(form_picture)
    size = (75,75)
    i.thumbnail(size)
    i.save(picture_path)
    return pic_fn