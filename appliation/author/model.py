from application import db
from datetime import datetime
from flask_sqlalchemy import *
class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.String(50), nullable=False, unique=True)
    blogs = db.relationship('Blog', backref='author', lazy=True)
class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blog_title = db.Column(db.String(500), nullable=False)
    blog_heading = db.Column(db.String(500), nullable=False)
    blog_content = db.Column(db.Text, nullable=False)
    blog_published_time = db.Column(db.DateTime, default=datetime.now())
    blog_scrap_time = db.Column(db.DateTime, default=datetime.now())
    blog_news_site = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'), nullable=False)
def CreateAll():
    db.create_all()

def dropAll():
    db.drop_all()
def InsertData(name, story_title, story_heading, story_content, timestamp, story_site):
    blog_result = Blog.query.filter_by(blog_title=story_title).first()
    if blog_result is not None:
        print("blog result is true")
        return True
    else:
        result = Author.query.filter_by(author_name=name).first()
        if result:
            blog = Blog(blog_title=story_title, blog_heading=story_heading, blog_content=story_content,
                        blog_published_time=timestamp, blog_news_site=story_site, author=result)
        else:
            author = Author(author_name=name)
            db.session.add(author)
            blog = Blog(blog_title=story_title, blog_heading=story_heading, blog_content=story_content,
                        blog_published_time=timestamp, blog_news_site=story_site, author=author)
        db.session.add(blog)
        db.session.commit()
        return False
