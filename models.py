
from config import db, bcrypt
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    _password_hash = db.Column(db.String, nullable = False)

    #Users in relation to various tasks, deletes both user and tasks incase user is deleted
    tasks = db.relationship('Task',  backref = 'user', cascade = 'all, delete-orphan')

    @hybrid_property
    def password_hash(self):
        #blocks password hashes from outside the class
        raise AttributeError('Password Hashes cannot be viewed')

    @password_hash.setter
    def password_hash(self, password):
        #Hashes password before storage
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        #Compares plaintext to hashed stored password
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username.strip()) == 0:
            raise ValueError('Username cannot be empty')
        return username

    def to_dict(self):
        #Excludes password, data is sent to the client
        return{
            'id': self.id,
            'username': self.username
        }

    def __repr__(self):
        return f"<User {self.username}>"

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #Foreign key tying tasks to one user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty!")
        return title

    def to_dict(self):
        return{
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id

        }

    def __repr__(self):
        return f"<Task {self.id}: {self.title}"



