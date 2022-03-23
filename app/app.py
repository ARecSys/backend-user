from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db, Favorite

load_dotenv()

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}?sslmode=require'.format(
    dbuser=os.getenv('DB_USER'),
    dbpass=os.getenv('DB_PASSWORD'),
    dbhost=os.getenv('DB_HOSTNAME'),
    dbname=os.getenv('DB_NAME')
)

app = Flask(__name__)
CORS(app)



app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.config.from_object(os.environ['APP_SETTINGS'])


db.init_app(app)

with app.app_context():
    #Favorite.__table__.drop(db.engine) # code to drop a table while waiting to be able to drop it on azure studio
    db.create_all()

from routes.routes_auth import *
from routes.routes_articles import *
from routes.routes_fav import *
from routes.routes_reco import *

# app.run(host='0.0.0.0', port=8080)

# if __name__ == '__main__':
#     app.run(debug=True)
