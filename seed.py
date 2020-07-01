from models import User, db
from app import app

db.drop_all()
db.create_all()

PostTag.query.delete()
Tag.query.delete()
Post.query.delete()
User.query.delete()

gary = User(first_name="Gary", last_name="Bobary",
            image_url="https://www.thesprucepets.com/thmb/MZcIufmv4DQ6QlSYy6YBmo0Pzg4=/3435x2576/smart/filters:no_upscale()/horse-galloping-in-grass-688899769-587673275f9b584db3a44cdf.jpg")

barry = User(first_name="Barry", last_name="Grace",
             image_url="https://suindependent.com/wp-content/uploads/2019/11/Cougar-sightings-on-the-rise-follow-these-tips-to-prevent-cougar-attacks.jpg")

jenny = User(first_name="Jenny", last_name="Bobenny")
jerry = User(first_name="Jerry", last_name="Bobary",
             image_url="https://www.channelfutures.com/files/2020/02/Nerd-877x432.jpg")


post1 = Post(title="Post1", content="Post One.", user_id=1)
post2 = Post(title="Post2", content="Post Two.", user_id=2)
post3 = Post(title="Post3", content="Post Three.", user_id=1)
post4 = Post(title="Post4", content="Post Four.", user_id=3)
post5 = Post(title="Post5", content="Post Five.", user_id=4)

tag1 = Tag(name='Funny', post_id=1)
tag2 = Tag(name='Sad', post_id=2)
tag3 = Tag(name='Thoughtful', post_id=1)
tag4 = Tag(name='Tutorial', post_id=3)

users = [gary, barry, jenny, jerry]
posts = [post1, post2, post3, post4, post5]
tags = [tag1, tag2, tag3, tag4]

db.session.add_all(users)
db.session.add_all(posts)
db.session.add_all(tags)

db.session.commit()
