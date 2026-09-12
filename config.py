import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

load_dotenv()

#flask instance
app = Flask(__name__)

#~~~~~~~~ Database config ~~~~~~~~#
database_url = os.environ.get('DATABASE_URL', 'sqlite:///app.db')

#~~~~~~~~ Render's PostgreSQL URL ~~~~~~~~#
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI']= database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#~~~~~~~~ JWT config ~~~~~~~~# 
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

# extensions initializations
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)
jwt = JWTManager(app)
CORS(app)





