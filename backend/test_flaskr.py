import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://raees:12345@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['questions'])

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        categories = {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
        }
        self.assertEqual(response.status_code, 200)

    def test_delete_question_exist(self):
        response = self.client().delete('/questions/5')
        data = json.loads(response.data)

        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['deleted'], 5)

    def test_delete_question_non_exist(self):
        response = self.client().delete('/questions/2000')
        data = json.loads(response.data)

        self.assertFalse(data['success'])
        self.assertEqual(response.status_code, 404)

    def test_add_question(self):
        question = {
            'question': 'What is the capital of Nigeria',
            'answer': 'Lagos',
            'difficulty': 2,
            'category': 3
        }
        response = self.client().post('/questions', json=question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_add_question_error(self):
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_search_question(self):
        response = self.client().post('/questions', json={'searchTerm': 'capital'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 1)

    def test_search_question_error(self):
        response = self.client().post('/questions', json={'searchTerm': 'ahbjndd'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 0)

    def test_search_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 3)

        # Second searach
        response2 = self.client().get('/categories/2/questions')
        data = json.loads(response2.data)

        self.assertEqual(response2.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 4)

    def test_search_by_category_nonexistance(self):
        response = self.client().get('/categories/100/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_start_quiz(self):
        response = self.client().post('/quizzes', json={'quiz_category': {}, 'previous_questions': []})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        self.assertTrue(isinstance(data['question'], dict))

    def test_start_quiz_error(self):
        response = self.client().post('/quizzes')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()