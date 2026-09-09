
from config import app, db
from models import User, Task

if __name__ == '__main__':
    app.run(port=5555, debug=True)