from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

gary = User(first_name="Gary", last_name="Bobary",
            image_url="https://www.thesprucepets.com/thmb/MZcIufmv4DQ6QlSYy6YBmo0Pzg4=/3435x2576/smart/filters:no_upscale()/horse-galloping-in-grass-688899769-587673275f9b584db3a44cdf.jpg")

barry = User(first_name="Barry", last_name="Grace",
             image_url="https://suindependent.com/wp-content/uploads/2019/11/Cougar-sightings-on-the-rise-follow-these-tips-to-prevent-cougar-attacks.jpg")

jenny = User(first_name="Jenny", last_name="Bobenny")
jerry = User(first_name="Jerry", last_name="Bobary",
             image_url="https://www.channelfutures.com/files/2020/02/Nerd-877x432.jpg")

db.session.add(gary)
db.session.add(barry)
db.session.add(jenny)
db.session.add(jerry)

db.session.commit()
