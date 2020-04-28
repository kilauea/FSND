import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  def paginate_selection(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formated_selection = [el.format() for el in selection]
    current_selection = formated_selection[start:end]
    if len(current_selection) == 0:
      abort(404)

    return current_selection
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    selection = Category.query.order_by(Category.id.asc()).all()
    categories_page = paginate_selection(request, selection)

    return jsonify({
      'success': True,
      'categories': categories_page,
      'total_categories': len(selection)
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    selection = Question.query.order_by(Question.id.asc()).all()
    questions_page = paginate_selection(request, selection)
    categories = Category.query.order_by(Category.id.asc()).all()

    return jsonify({
      'success': True,
      'questions': questions_page,
      'total_questions': len(Question.query.all()),
      'categories': {category.id: category.type for category in categories},
      'current_category': 1
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      if question is None:
        abort(404)

      question.delete()

      selection = Question.query.order_by(Question.id.asc()).all()
      questions_page = paginate_selection(request, selection)
      categories = Category.query.order_by(Category.id.asc()).all()
      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': questions_page,
        'total_questions': len(Question.query.all()),
        'categories': {category.id: category.type for category in categories},
        'current_category': 1
      })
    except:
      print(sys.exc_info())
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def create_and_search_questions():
    body = request.get_json()
    try:
      if 'searchTerm' in body:
        # Search a question based on searchTerm
        search_term = body.get('searchTerm', None)
        if search_term == '':
          abort(422)
        questions = Question.query.filter(Question.question.ilike('%' + search_term + '%'))
        return jsonify({
          'success': True,
          'questions': paginate_selection(request, questions),
          'total_questions': len(Question.query.all()),
          'current_category': 1
        })
      else:
        # Create a new question
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        if not (question and answer):
          abort(422)
        new_question = Question(
          question=question,
          answer=answer,
          category=category,
          difficulty=difficulty
        )
        new_question.insert()
        return jsonify({
          'success': True
        })
    except:
      print(sys.exc_info())
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:categoty_id>/questions', methods=['GET'])
  def get_questions_per_category(categoty_id):
    questions = Question.query.filter(Question.category == categoty_id).all()
    if questions is None:
      abort(404)
    questions_page = paginate_selection(request, questions)

    return jsonify({
      'success': True,
      'questions': questions_page,
      'total_questions': len(Question.query.all()),
      'current_category': 1
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  return app

if __name__ == '__main__':
  app = create_app()
  app.run(debug=True)