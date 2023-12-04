import json
import unittest
from main import app, db
from models import Category
from unittest import mock


class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:MiUniDB@localhost/AudiobookStoreTestDatabase'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @mock.patch('routers.auth.token_required', lambda x: x)
    def test_add_category(self):
        data = {'category_name': 'New Category'}
        response = self.client.post('/category/', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Category added', response.json['message'])


    @mock.patch('routers.auth.token_required', lambda x: x)
    def test_get_categories(self):
        # Add test data
        with self.app.app_context():
            db.session.add(Category(category_name='Test Category'))
            db.session.commit()

        response = self.client.get('/category/')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['category_name'], 'Test Category')


    @mock.patch('routers.auth.token_required', lambda x: x)
    def test_delete_category(self):
        # Add test data
        with self.app.app_context():
            category = Category(category_name='Test Category')
            db.session.add(category)
            db.session.commit()
            category_id = category.id

        response = self.client.delete(f'/category/{category_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Category deleted', response.json['message'])

    def test_update_category(self):
        # Add test data
        with self.app.app_context():
            category = Category(category_name='Old Category')
            db.session.add(category)
            db.session.commit()
            category_id = category.id

        data = {'category_name': 'Updated Category'}
        response = self.client.put(f'/category/{category_id}', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Category updated', response.json['message'])

        with self.app.app_context():
            category = Category.query.get(category_id)
            self.assertEqual(category.category_name, 'Updated Category')

if __name__ == '__main__':
    unittest.main()
