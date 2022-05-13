import random

from faker import Faker

from models.database import get_db, User, Blog, Post, Subscribe

fake = Faker()
db = next(get_db())


def load_data_db():
    for _ in range(1_000):
        user = User(username=fake.name())
        blog = Blog(user=user)
        db.add(user)
        db.commit()

    for _ in range(1_000):
        post = Post(blog_id=random.randint(1, 1_000),
                    title=fake.word(),
                    text=fake.text(max_nb_chars=140))

        db.add(post)
        db.commit()

    for _ in range(1_000):
        user = db.query(User).get(random.randint(1, 1_000))
        for _ in range(1, 10):
            subscribe = Subscribe(user_id=random.randint(1, 1_000), blog_id=random.randint(1, 1_000))
            user.subscribers.append(subscribe)
        db.add(user)
        db.commit()
