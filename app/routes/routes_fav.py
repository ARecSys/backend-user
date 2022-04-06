from asyncio.log import logger
import logging
from app import app
from models import Article, Favorite, User, db
from flask import request, jsonify, make_response
from utils.auth import token_required
from utils.recommendation import send_msg_to_queue


@app.route('/api/fav/list', methods =['GET']) 
@token_required
def get_fav_list(user): 
    public_id = user.public_id

    favorites = Favorite.query.filter_by(user=public_id ).all()

    if not favorites: 
        
        return make_response( 
            'No favs',
            401
        ) 
    
   
    serialized_favorites = [x.serialize() for x in favorites]

    return jsonify(serialized_favorites ) 


@app.route('/api/fav/add', methods =['POST']) 
@token_required
def add_fav(user):
    data = request.args
    doi = data["doi"]
    public_id = user.public_id

    favorite = Favorite.query.filter_by( id = public_id+" "+doi ).first()

    if not favorite: 

        article = Article.query.filter_by(doi = data["doi"]).first()
        
        favorite = Favorite( 
            id = public_id+" "+doi,
            user = public_id,
            doi = doi,
            title = article.title
        ) 
        
        db.session.add(favorite) 
        db.session.commit() 
    
        send_msg_to_queue(public_id)

        return make_response('Successfully registered.', 201) 

    else: 
        return make_response('Fav already exists.', 202) 

@app.route('/api/fav/delete', methods =['POST']) 
@token_required
def del_fav(user): 
    data = request.args
    doi = data["doi"]
    public_id = user.public_id

    favorite = Favorite.query.filter_by( id = public_id+" "+doi ).first()

    if favorite: 

        db.session.delete(favorite) 
        db.session.commit() 
    
        send_msg_to_queue(public_id)

        return make_response('Successfully deleted.', 201) 

    else: 
        return make_response('Fav does not exist.', 202) 