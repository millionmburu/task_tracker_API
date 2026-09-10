
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

#flask instance
app = Flask(__name__)

#~~~~~~~~ Database config ~~~~~~~~#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#~~~~~~~~ JWT config ~~~~~~~~# 
# TODO replace with  the actual JWT key
app.config['JWT_SECRET_KEY'] = '013kfsiekadpad'

# extensions initializations
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)
jwt = JWTManager(app)
CORS(app)





