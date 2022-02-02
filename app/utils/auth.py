from flask import request, jsonify, make_response
import json
from functools import wraps
import jwt
from models import User, db
from app import app

def token_required(f): 
    @wraps(f) 
    def decorated(*args, **kwargs): 
        token = None

        if 'x-access-token' in request.headers: 
            token = request.headers['x-access-token'] 
        if not token: 
            return jsonify({'message' : 'Token is missing !!'}), 401
   
        try: 
        
            data = jwt.decode(token, app.config['SECRET_KEY'], "HS256") 
            current_user = User.query.filter_by(public_id = data['public_id']).first() 
        except Exception as Argument:
            return jsonify({ 
                'message' : 'Token is invalid !!'
            }), 401
        
        return  f(current_user, *args, **kwargs) 
   
    return decorated 