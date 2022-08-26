import os
import sys
from flask import Flask, request, abort, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r'/': {'origins': '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')

        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()            
        return jsonify({
          'categories':  {str(c.id): c.type for c in categories}
        })



    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, int)
        questions = Question.query.all()
        categories = Category.query.all()
        formated_questions = [q.format() for q in questions]

        per_page = 10
        start = (page - 1) * 10
        end = page * per_page

        if len(formated_questions[start:end]) == 0:
            abort(404)            

        return jsonify({
            'success': True,
            'total_questions': len(questions),
            'questions': formated_questions[start:end],
            'categories':  {str(c.id): c.type for c in categories}
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', 1)

        # if request contains search term redirect to
        # search_question route
        if body.get('searchTerm'):
            return search_question(body.get('searchTerm'))
        
        if not (question or answer):
            abort(400)

        try:
            category = Category.query.get(int(category))
            new_question = Question(question, answer, category.id, difficulty)
            new_question.insert()
            
            return jsonify({
                'success': True,
                'created': new_question.id
            })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    def search_question(search_term):
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        formated_questions = [q.format() for q in questions]
        
        return jsonify({
            'success': True,
            'questions': formated_questions,
            'total_questions': len(questions)
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def search_by_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        if not questions:
            abort(404)
        formated_questions = [q.format() for q in questions]
        currentCategory = Category.query.get(category_id).type

        return jsonify({
            'success': True,
            'questions': formated_questions,
            'total_questions': len(questions),
            'current_category': currentCategory
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def start_quiz():
        body = request.get_json()
        if not body:
            abort(400)

        category = body.get('quiz_category')['id']
        previous_questions = body.get('previous_questions', [])
        print(previous_questions)

        
        try:
            if category:
                questions = Question.query.filter_by(category=category).all()
            else:
                questions = Question.query.all()

            filtered = [x for x in questions if x.id not in previous_questions]
            if filtered:
                question = random.choice(filtered)
                return jsonify({
                    'success': True,
                    'question': question.format(),
                    'previous_questions': previous_questions
                })
            else:
                return jsonify({
                    'success': True,
                    'question': False,
                    'previous_questions': previous_questions
                })

            
        except:
            print(sys.exc_info())
            abort(422)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(code):
        return jsonify({
            'success': False,
            'message': 'not found',
            'error': 404
        }), 404

    @app.errorhandler(400)
    def bad_request(code):
        return jsonify({
            'success': False,
            'message': 'bad request',
            'error': 400

        }), 400

    @app.errorhandler(422)
    def unprocessed(code):
        return jsonify({
            'success': False,
            'message': 'request unprocessed',
            'error': 422
        }), 422

    @app.errorhandler(500)
    def server_error(code):
        return jsonify({
            'success': False,
            'message': 'internal server error',
            'error': 500
        }), 500


    return app

