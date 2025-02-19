from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Test the views for users."""

    def setUp(self):
        """Add sample user and sample post."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title="TestPost", content="Test Post.",
                    user_id=self.user_id)

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Clean up."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)

    def test_show_user(self):
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)

    def test_new_user_form(self):
        with app.test_client() as client:
            res = client.get("/users/new")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Add A User</h1>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            res = client.post(f"/users/{self.user_id}/delete",
                              data={"user_id": "{self.user_id}"},
                              follow_redirects=True)

            self.assertEqual(res.status_code, 200)


class PostViewsTestCase(TestCase):
    """Test the views for posts."""

       def test_new_post_form(self):
            with app.test_client() as client:
                res = client.get("/users/{self.user_id}/posts/new")
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('<h1>Add A Post for Test User</h1>', html)

        def test_edit_post_form():
          with app.test_client as client:
            res. = client.get("/posts/{self.post_id}/edit")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status.code, 200)
            self.assertIn('<h1>Edit Post</h1>', html)

        def test_delete_post(self):
            with app.test_client() as client:
                res = client.post(f"/posts/{self.post_id}/delete",
                                  data={"post_id": "{self.post_id}"},
                                  follow_redirects=True)

                self.assertEqual(res.status_code, 200)

        
