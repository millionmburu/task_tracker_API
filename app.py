
from config import app, db, api
from models import User, Task
from resources.auth import SignUp, Login,Me

#Connects the resource classes to a URL
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Me, '/me')

if __name__ == '__main__':
    app.run(port=5555, debug=True)