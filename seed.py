
from faker import Faker
from config import db, app
from models import User, Task

fake = Faker()

with app.app_context():
    print("Clearing existing data.....")
    Task.query.delete()
    User.query.delete()
    db.session.commit()

    print("Seeding users...")
    users = []

    for _ in range(3):
        user = User(username= fake.unique.user_name()) #fake prevents duplaication of username keeping it unique
        user.password_hash = "password123" #Easy password for testing
        users.append(user)
        db.session.add(user)
    db.session.commit()

    print("Seeding tasks.....")
    for user in users:
        for _ in range(5):
            task = Task(
                title = fake.sentence(nb_words=4),
                description= fake.text(max_nb_chars=100),
                completed= fake.boolean(),
                user_id = user.id
            )
            db.session.add(task)
    db.session.commit()

    for user in users:
        print(f"{user.username} (id={user.id}) - password: password123")

    print("Seeding completed")
