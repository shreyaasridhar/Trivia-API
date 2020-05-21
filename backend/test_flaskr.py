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
        self.database_name = "test_trivia"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        self.new_question = {
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
            "answer": "Edward Scissorhands",
            "difficulty": 3,
            "category": 5
        }
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

    # Test for GET '/categories'

    def test_view_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
        self.assertTrue(data['total_categories'])

    def test_404_categories(self):
        res = self.client().get('/categories?page=10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource not found')
        self.assertFalse(data['success'])

    #  Test for GET '/questions'

    def test_retrive_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertEqual(data["current_category"], None)

    def test_404_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource not found')
        self.assertFalse(data['success'])

    # Test for DELETE '/questions/<question_id>'

    def test_delete_question(self):
        res = self.client().delete('/questions/25')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 25).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(question, None)

    def test_400_delete(self):
        res = self.client().delete('/questions/2400')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable request')
        self.assertFalse(data['success'])

    # Test for POST '/questions' to add questions

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Test for POST '/questions' to searchTerm

    def test_search_question_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'Tom'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 1)

    # Test for GET '/catergories/{category_id}/questions'

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertEqual(data["current_category"], 5)

    # Test for POST '/quizzes'

    def test_quiz(self):
        res = self.client().post('/quizzes',
                                 json={"quiz_category": {"type": "Science", "id": 1}, "previous_questions": []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["question"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
