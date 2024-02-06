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

    #   use this path when submitting project for review
    #   self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

    #   use this path when running with local postgres server
        self.database_path = 'postgresql://rock:123@localhost:5432/trivia_test'
        
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

#  ----------------------------------------------------------------
#  Tests related to Category GET
#  ----------------------------------------------------------------

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)

#  ----------------------------------------------------------------
#  Tests related to Questions GET
#  ----------------------------------------------------------------

    def test_get_questions_default_page(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(len(data['categories']), 6)
        self.assertTrue(data['currentCategory'])
        self.assertTrue(data['totalQuestions'] > 0)

    def test_get_questions_proper_pagenation(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 9)
        self.assertEqual(len(data['categories']), 6)
        self.assertTrue(data['currentCategory'])
        self.assertTrue(data['totalQuestions'] > 0)

    def test_get_questions_invalid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_category_questions(self):
        n = 1
        while n < 7:
            res = self.client().get('/categories/' + str(n) + '/questions')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(len(data['questions']) > 0)
            self.assertTrue(data['currentCategory'])
            self.assertTrue(data['totalQuestions'] > 0)
            n += 1

    def test_get_invalid_category_questions(self):
        res = self.client().get('/categories/7/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#  ----------------------------------------------------------------
#  Tests related to New Question POST
#  ----------------------------------------------------------------

    def test_post_question_with_proper_format(self):
        res = self.client().post('/questions', 
                json={
                    'question': 'Does this work?',
                    'answer': 'I hope so!',
                    'difficulty': 5,
                    'category': 1
                }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
        self.assertTrue(data['totalQuestions'] > 0)
        """ next delete the question so the database doesn't grow with each test run"""
        new_id = data['created']
        res = self.client().delete('/questions/' + str(new_id))

    def test_post_question_missing_question(self):
        res = self.client().post('/questions', 
                json={
                    'answer': 'What is the question?',
                    'difficulty': 5,
                    'category': 1
                }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])


    def test_post_question_missing_answer(self):
        res = self.client().post('/questions', 
                json={
                    'question': 'Does this work?',
                    'difficulty': 5,
                    'category': 1
                }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_post_question_with_invalid_difficulty(self):
        res = self.client().post('/questions', 
                json={
                    'question': 'Does this work?',
                    'answer': 'I hope not!',
                    'difficulty': 10,
                    'category': 1
                }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_post_question_with_invalid_category(self):
        res = self.client().post('/questions', 
                json={
                    'question': 'Does this work?',
                    'answer': 'I hope not!',
                    'difficulty': 3,
                    'category': 7
                }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

#  ----------------------------------------------------------------
#  Tests related to Questions search POST
#  ----------------------------------------------------------------

    def test_post_question_search_hit(self):
        res = self.client().post('/search', json={'searchTerm': 'who'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['totalQuestions'], 3)

    def test_post_question_search_miss(self):
        res = self.client().post('/search', json={'searchTerm': 'udacity'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_post_question_search_term_null(self):
        res = self.client().post('/search', json={'searchTerm': ''})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

#  ----------------------------------------------------------------
#  Tests related to Question DELETE
#  ----------------------------------------------------------------

    def test_delete_question_with_valid_id(self):
        """ first add a dummy question to the db"""
        res = self.client().post('/questions', 
                json={
                    'question': 'How long will this question last in the db?',
                    'answer': 'Not long!',
                    'difficulty': 5,
                    'category': 1
                }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
        self.assertTrue(data['totalQuestions'] > 0)
        temp_total = data['totalQuestions']
        new_id = data['created']
        """ next delete the dummy question"""
        res = self.client().delete('/questions/' + str(new_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual((temp_total - data['totalQuestions']), 1)

    def test_delete_question_with_invalid_id(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_delete_question_with_invalid_method(self):
        res = self.client().patch('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])

#  ----------------------------------------------------------------
#  Tests related to Game Play
#  ----------------------------------------------------------------

    def test_post_play_all(self):
         res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': "click", 'id': 0}})
         data = json.loads(res.data)
         self.assertEqual(res.status_code, 200)
         self.assertTrue(data['success'])
         self.assertEqual(len(data['question']), 5)

    def test_post_play_valid_category(self):
         n = 1
         while n < 7:
            res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': "", 'id': n}})
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(len(data['question']), 5)
            n += 1

    def test_post_play_invalid_category(self):
            res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': "", 'id': 10}})
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 422)
            self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()