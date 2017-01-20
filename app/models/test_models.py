import datetime
import unittest
from app import db
from app.test_config import GlobalTestCase
from .bucketlist_models import Bucketlists, Users, Items


class ModelsTest(GlobalTestCase):
    """In this class we will be testing all models: Bucketlist
Users and Items, it contains tests for: Creating/Editing/Deleting
items.
    """

    def setUp(self):
        db.create_all()
        self.user = Users(
            username="johndoe",
            email="johndoe@andela.com",
            password="J0hny123")
        db.session.add(self.user)
        db.session.commit()
        user = Users.query.filter_by(username='user1').first()
        self.bucketlist = Bucketlists(
            name="Maasai Mara",
            description="Go see the big 5",
            date_created=datetime.datetime.utcnow(),
            creator_id=user.user_id
        )
        db.session.add(self.bucketlist_items)
        db.session.commit()

    def test_can_create_user(self):
        user = Users.query.filter_by(username='user1').first()
        self.assertIsInstance(self.user, Users)
        self.assertIsNotNone(user.username)
        self.assertEqual(user.email, 'user@andela.com')

    def test_can_edit_user(self):
        self.user.email = 'user@gmail.com'
        db.session.merge(self.user)
        db.session.commit()
        user = Users.query.filter_by(username='user').first()
        self.assertEqual(user.email, 'user@gmail.com')

    def test_can_create_bucketlist(self):
        bucketlist = Bucketlists.query.filter_by(name='Maasai Mara').first()
        self.assertIsInstance(self.bucketlist, Bucketlists)
        self.assertIsNotNone(bucketlist.name)
        self.assertEqual(bucketlist.name, "Maasai Mara")

    def test_can_edit_bucketlist(self):
        self.bucketlist.name = "Fort Jesus"
        db.session.add(self.bucketlist)
        db.session.commit()
        item = Items.query.filter_by(name="Kruger Park").first()
        self.assertEqual(item.name, "Kruger Park")

    def test_can_delete_item_in_bucketlist(self):
        db.session.delete(self.bucketlist_items)
        db.session.commit()
        item = Items.query.filter_by(name="Kruger Park").first()
        self.assertEqual(item, None)

    def tearDown(self):
        db.session.close_all()
        db.session.drop_all()


if __name__ == '__main__':
    unittest.main()
