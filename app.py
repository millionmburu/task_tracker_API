
from config import app, db, api
from models import User, Task

from resources.auth import SignUp, Login,Me
from resources.tasks import TaskList, TaskDetail

#Connects the resource classes to a URL
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Me, '/me')

# CRUD routes
api.add_resource(TaskList, '/tasks')
api.add_resource(TaskDetail, '/tasks/<int:task_id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)