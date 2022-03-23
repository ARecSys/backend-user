from app import app
from models import User, db
from flask import request, jsonify
from utils.recommendation import send_msg_to_queue
from utils.http_status_code import HttpStatusCode
from utils.backend_status_code import BackendStatusCode

@app.route('/api/reco/msg', methods =['POST']) 
def msg(): 
    
    reco_sc = BackendStatusCode.ERROR
    http_sc = HttpStatusCode.BAD_REQUEST

    data = request.get_json()
    
    if data:
        
        if data['public_id']:
            
            user = User.query.filter_by( public_id = data['public_id'] ).first()
            
            if user:
                ret = send_msg_to_queue ( data['public_id'] )
                
                reco_sc = BackendStatusCode.OK
                http_sc = HttpStatusCode.OK
            
            else:

                reco_sc = BackendStatusCode.USER_NOT_FOUND
                http_sc = HttpStatusCode.UNAUTHORIZED
        
        else:
            reco_sc = BackendStatusCode.USER_NOT_FOUND
            http_sc = HttpStatusCode.BAD_REQUEST
    
    else:

        reco_sc = BackendStatusCode.DATA_NOT_FOUND
        http_sc = HttpStatusCode.BAD_REQUEST
    
    return jsonify  (   { 
                            "BackendStatusCode" : reco_sc
                        }
                    ), int ( http_sc )
