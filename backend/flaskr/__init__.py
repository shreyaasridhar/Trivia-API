import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]

    return questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def view_categories():
        selection = Category.query.order_by(Category.id).all()
        category = paginate(request, selection)
        if len(category) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "categories": {c['id']: c['type'] for c in category},
            "total_categories": len(selection)
        })

    @app.route('/questions')
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_question = paginate(request, selection)
        if len(current_question) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": current_question,
            "total_questions": len(selection),
            "categories": {category.id: category.type for category in Category.query.order_by(Category.id).all()},
            "current_category": None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question == None:
            abort(422)
        question.delete()
        return jsonify({
            "success": True
        })

    @app.route('/questions', methods=["POST"])
    def create_question():
        data = request.get_json()
        if not data:
            abort(422)
        if 'searchTerm' in data:
            search = data['searchTerm']
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(search)))
            searches = paginate(request, selection)
            return jsonify({
                'success': True,
                'questions': searches,
                'total_questions': len(searches),
                'current_category': None
            })
        else:
            question = data['question']
            answer = data['answer']
            difficulty = data['difficulty']
            category = data['category']
            Question(question=question, answer=answer,
                     difficulty=difficulty, category=category).insert()
            return jsonify({
                "success": True
            })

    @app.route('/categories/<int:category_id>/questions')
    def questions_category(category_id):
        questions = Question.query.order_by(Question.id).filter(
            Question.category == category_id).all()
        current_questions = paginate(request, questions)
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": current_questions,
            'total_questions': len(current_questions),
            "current_category": category_id
        })

    @app.route('/quizzes', methods=["POST"])
    def render_questions():
        data = request.get_json()
        if not data:
            abort(422)
        previousQuestions = data['previous_questions']
        category = data['quiz_category']['id']
        if category == 0:
            currentQuestion = Question.query.filter(
                Question.id.notin_(previousQuestions)).all()
        else:
            currentQuestion = Question.query.filter(
                Question.category == data['quiz_category']['id']).filter(Question.id.notin_(previousQuestions)).all()
        if len(currentQuestion) == 0:
            return jsonify({
                'success': True,
                'question': None
            }), 200

        return jsonify({
            "success": True,
            "question": random.choice(currentQuestion).format()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            "message": 'Resource not found',
            "error": 404
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            "message": 'Unprocessable request',
            "error": 422
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    return app
