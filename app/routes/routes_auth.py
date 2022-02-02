from app import app
from models import User, db
from flask import request, jsonify, make_response
import json
from functools import wraps
import jwt
import uuid 
import os
from  werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime, timedelta 

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
 
@app.route('/')
def index():
    return 'Web App A recsys!'


@app.route('/api/users/login', methods =['POST']) 
def login(): 
    
    auth = request.get_json()
   
   
    if not auth or not auth['email'] or not auth['password']: 
        
        return make_response( 
            'Could not verify', 
            401, 
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'} 
        ) 
   
    user = User.query.filter_by(email = auth['email']).first() 
   
    if not user: 
        
        return make_response( 
            'Could not verify', 
            401, 
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'} 
        ) 
   
    if check_password_hash(user.password, auth['password']): 
        
        token = jwt.encode({ 
            'public_id': user.public_id, 
            'exp' : datetime.utcnow() + timedelta(minutes = 30000) 
        }, app.config['SECRET_KEY']) 
   
        return make_response(jsonify({'token' : token}), 201) 
    
    return make_response( 
        'Could not verify', 
        403, 
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'} 
    ) 
   
@app.route('/api/users/register', methods =['POST']) 
def register(): 
    
    data = request.get_json()
   

    
    email = data['email']
    password = data['password']

    app.logger.info(json.dumps( request.get_json()))

    app.logger.info(password)
   
    
    user = User.query.filter_by(email = email).first() 
    if not user: 
        
        user = User( 
            public_id = str(uuid.uuid4()), 
            email = email, 
            password = generate_password_hash(password) 
        ) 
        
        db.session.add(user) 
        db.session.commit() 
   
        return make_response('Successfully registered.', 201) 
    else: 
        
        return make_response('User already exists. Please Log in.', 202) 
