from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
import jwt
import uuid 
from  werkzeug.security import generate_password_hash, check_password_hash 
from flask_sqlalchemy import  SQLAlchemy
from datetime import datetime, timedelta 
from functools import wraps
from dotenv import load_dotenv

import json

load_dotenv()

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}?sslmode=require'.format(
    dbuser=os.getenv('DB_USER'),
    dbpass=os.getenv('DB_PASSWORD'),
    dbhost=os.getenv('DB_HOSTNAME'),
    dbname=os.getenv('DB_NAME')
)

app = Flask(__name__)
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#todel

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    public_id = db.Column(db.String(50), unique = True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String())

#db.create_all()

@app.route('/')
def index():
    app.logger.info( json.dumps( os.environ['APP_SETTINGS']))
    return 'Web App A recsys!'

def token_required(f): 
    @wraps(f) 
    def decorated(*args, **kwargs): 
        token = None
        
        if 'x-access-token' in request.headers: 
            token = request.headers['x-access-token'] 
        
        if not token: 
            return jsonify({'message' : 'Token is missing !!'}), 401
   
        try: 
            
            data = jwt.decode(token, app.config['SECRET_KEY']) 
            current_user = User.query.filter_by(public_id = data['public_id']).first() 
        except: 
            return jsonify({ 
                'message' : 'Token is invalid !!'
            }), 401
        
        return  f(current_user, *args, **kwargs) 
   
    return decorated 


@app.route('/api/user', methods =['GET']) 
@token_required
def get_all_users(current_user): 
    
    
    users = User.query.all() 
    
    
    output = [] 
    for user in users: 
        
        output.append({ 
            'public_id': user.public_id, 
            'name' : user.name, 
            'email' : user.email 
        }) 
   
    return jsonify({'users': output}) 

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
            'exp' : datetime.utcnow() + timedelta(minutes = 30) 
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


app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    app.run(debug=True)
