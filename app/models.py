from flask_sqlalchemy import  SQLAlchemy
from dataclasses import dataclass


db = SQLAlchemy()

@dataclass
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    public_id = db.Column(db.String(50), unique = True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String())

    def serialize(self):
        return { 
            "id" : self.id, 
            "public_id" : self.public_id, 
            "email" : self.email
        }


@dataclass
class Favorite(db.Model):
    __tablename__ = 'fav_articles'
    id = db.Column(db.String(100), primary_key = True) 
    user = db.Column(db.String(50)) 
    doi = db.Column(db.String(100))
    title = db.Column(db.String(100))

    def serialize(self):
        return { 
            "user" : self.user, 
            "doi" : self.doi,
            "title" : self.title
        }


@dataclass
class Article(db.Model):
    __tablename__ = 'articles_metadata'

    id = db.Column(db.String(50), primary_key = True) 
    doi = db.Column(db.String(100))
    title = db.Column(db.String())
    authors = db.Column(db.ARRAY(db.String))
    keywords = db.Column(db.ARRAY(db.String))
    fos =  db.Column(db.ARRAY(db.String))
    references = db.Column(db.ARRAY(db.String))

    def __repr__(self):
        return "<Article(doi='%s', id='%s', title='%s', authors='%s')>" % (
                                self.doi, self.id, self.title, self.authors )

    def serialize(self):
        return { 
            "doi" : self.doi, 
            "title" : self.title, 
            "authors" : self.authors, 
            "keywords" :  self.keywords, 
            "fos" :  self.fos, 
            "references" : self.references }