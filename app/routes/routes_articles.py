from asyncio.log import logger
import json
import logging
from app import app
from models import Article, User, db
from flask import request, jsonify, make_response
from utils.auth import token_required

@app.route('/api/article', methods =['GET']) 
@token_required
def get_article_doi(user):

    data = request.args

    article = Article.query.filter_by(doi = data["doi"]).first() 

    if not article: 
        
        return make_response( 
            'No articles', 
            401
        ) 
   
    return jsonify(article.serialize()) 


@app.route('/api/article/neighbors', methods =['GET']) 
@token_required
def get_article_neighbors(user): 
    data = request.args

    article = Article.query.filter_by(doi = data["doi"]).first()

    if not article.references:
        return make_response( 
            'No references', 
            401
        ) 
    
    neighbors = Article.query.filter( Article.id.in_(article.references) ).all()

    if not neighbors: 
        
        return make_response( 
            'No articles', 
            401
        ) 
    
   
    serialized_neighbors = [x.serialize() for x in neighbors]
    return jsonify(serialized_neighbors) 
