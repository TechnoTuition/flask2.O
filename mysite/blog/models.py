class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),     nullable=False)
    content = db.Column(db.Text,nullable=False)
    post_created = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    
    def __repr__(self):
        return f"{self.title},{self.content},{self.post_created},{self.user_id}"