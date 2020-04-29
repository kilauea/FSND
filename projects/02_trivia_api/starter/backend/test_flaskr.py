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
    self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    self.new_question = {
      'question': 'Which country won the soccer World Cup in 2011',
      'answer': 'Spain',
      'category': '6',
      'difficulty': '2'
    }

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
  def test_get_categories(self):
    res = self.client().get('/categories')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(isinstance(data['categories'], dict))
    self.assertTrue(len(data['categories']))
    self.assertTrue(data['total_categories'])

  def test_get_questions(self):
    res = self.client().get('/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(data['questions']))
    self.assertTrue(data['total_questions'])
    self.assertTrue(isinstance(data['categories'], dict))
    self.assertTrue(len(data['categories']))
    self.assertTrue(data['current_category'])

  def test_404_get_questions_beyond_valid_page(self):
    res = self.client().get('/questions?page=0')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

  def test_delete_questions(self):
    # First we create a new question
    question = Question(**self.new_question)
    question.insert()
    # Now we query for the new question to delete it
    question = Question.query.filter(
      Question.question.like(
        '%' + self.new_question['question'] + '%'
      )
    ).one_or_none()
    self.assertTrue(question)
    id = question.id
    res = self.client().delete('/questions/' + str(id))
    data = json.loads(res.data)

    question = Question.query.filter(Question.id == id).one_or_none()

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['deleted'], id)
    self.assertTrue(len(data['questions']))
    self.assertTrue(data['total_questions'])
    self.assertTrue(isinstance(data['categories'], dict))
    self.assertTrue(len(data['categories']))
    self.assertTrue(data['current_category'])

  def test_404_delete_question_does_not_exist(self):
    res = self.client().delete('/questions/0')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

  def test_create_new_questions(self):
    # Try to create a new question
    res = self.client().post('/questions', json=self.new_question)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    
    # Delete the new question if created
    question = Question.query.filter(
      Question.question.like(
        '%' + self.new_question['question'] + '%'
      )
    ).one_or_none()
    if question:
      question.delete()

  def test_422_create_new_questions_without_question(self):
    fake_question = self.new_question
    fake_question['question'] = ''
    res = self.client().post('/questions', json=fake_question)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

  def test_422_create_new_questions_without_answer(self):
    fake_question = self.new_question
    fake_question['answer'] = ''
    res = self.client().post('/questions', json=fake_question)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

  def test_search_questions(self):
    res = self.client().post('/questions', json={'searchTerm': 'tom'})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(data['questions']))
    self.assertTrue(data['total_questions'])
    self.assertTrue(data['current_category'])

  def test_422_search_questions_without_search_term(self):
    res = self.client().post('/questions', json={'searchTerm': ''})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

  def test_get_questions_per_category(self):
    res = self.client().get('/categories/1/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(data['questions']))
    self.assertTrue(data['total_questions'])
    self.assertTrue(data['current_category'])

  def test_404_get_invalid_questions_per_category(self):
    res = self.client().get('/categories/0/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

  def test_create_quizzes(self):
    # Try to create a new quizze to play the game with all valid categories
    categories_id = [category.id for category in Category.query.all()]
    categories_id.append(0)
    for category_id in categories_id:
      quizze_query = {
        'previous_questions': [],
        'quiz_category': {'type': None, 'id': category_id}
      }
      res = self.client().post('/quizzes', json=quizze_query)
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['question'])
      self.assertTrue(isinstance(data['question'], dict))
      self.assertEqual(data['question']['category'] in categories_id, True)

  def test_404_create_quizzes_with_invalid_category(self):
    quizze_query = {
      'previous_questions': [],
      'quiz_category': {'type': None, 'id': -1}
    }
    res = self.client().post('/quizzes', json=quizze_query)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()