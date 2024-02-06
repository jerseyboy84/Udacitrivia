import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

questionsPerPage = 10
currentCategory = 1


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})    


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Content unprocessable"
        }), 422
    

    @app.route('/categories', methods=['GET'])
    def categories():
        try:
            categories = Category.query.all()
            formatted_categories = {}
            for category in categories:
                formatted_categories = dict(**formatted_categories, **category.altFormat())
            return jsonify({
                'success':True,
                'categories':formatted_categories
                })
        except:
            abort(422)

    @app.route('/questions', methods=['GET'])
    def questions():
        try:
            categories = Category.query.all()
            formatted_categories = {}
            for category in categories:
                formatted_categories = dict(**formatted_categories, **category.altFormat())
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * questionsPerPage
            end = start + questionsPerPage    
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]
            if formatted_questions[start:end] == []:
                abort(404)
            else:    
                return jsonify({
                    'success':True,
                    'questions':formatted_questions[start:end],
                    'totalQuestions':len(questions),
                    'currentCategory':categories[currentCategory-1].type,
                    'categories':formatted_categories
                    })
        except:
            abort(404)


    @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def catQuestions(cat_id):   
        try:
            currentCategory = cat_id
            categories = Category.query.all()
            questions = Question.query.filter(Question.category == currentCategory).all()
            formatted_questions = [question.format() for question in questions]
            if formatted_questions == []:
                abort(404)
            return jsonify({
                'success':True,  
                'questions':formatted_questions,
                'totalQuestions':len(questions),
                'currentCategory':categories[currentCategory-1].type
                })
        except:
            abort(404)


    @app.route('/questions', methods=['POST'])
    def newQuestion():   
        content = request.get_json()
        new_question = content.get('question', None)
        if new_question is None:
            abort(400)
        new_answer = content.get('answer', None)
        if new_answer is None:
            abort(400)
        new_difficulty = content.get('difficulty', None)
        if (new_difficulty is None) or (int(new_difficulty) < 1) or (int(new_difficulty) > 5):
            abort(400)
        new_category = content.get('category', None)
        if (new_category is None) or (int(new_category) < 1) or (int(new_category) > 6):
            abort(400)
        try:
            question = Question(question=new_question, answer=new_answer, 
                difficulty=new_difficulty, category=new_category)
            question.insert()
            questions = Question.query.all()
            return jsonify({
                'success':True,
                'created':question.id,
                'totalQuestions':len(questions)
                })
        except:
            abort(400)
      

    @app.route('/search', methods=['POST'])
    def search():   
        content = request.get_json()
        searchTerm = content.get('searchTerm', None)
        if searchTerm == "":
            abort(422)    
        try:
            questions = Question.query.filter(Question.question.ilike("%" + searchTerm + "%")).all()
            if questions == []:
                return jsonify({
                    'success':False, 
                    'error': 404,
                    'message': "No questions contain this text",
                    'questions':formatted_questions,
                    'totalQuestions':len(questions)
                    })
            formatted_questions = [question.format() for question in questions]
            return jsonify({
                'success':True, 
                'questions':formatted_questions,
                'totalQuestions':len(questions)
                })
        except:
            abort(404) 


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def deleteQuestion(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()        
            if question is None:
                abort(422)
            question.delete()
            questions = Question.query.all()
            return jsonify({
                'success':True,
                'totalQuestions':len(questions)
                })
        except:
            abort(422)
  

    @app.route('/quizzes', methods=['POST'])
    def nextQuestion():   
        content = request.get_json()
        prevQuestions = content['previous_questions']
        category_id = content['quiz_category']['id']
        category_type = content['quiz_category']['type']
        category = Category.query.get(category_id)
        try:
            if (category_type == 'click'):
                if prevQuestions is None:
                    questions = Question.query.all()
                else:
                    questions = Question.query.filter(Question.id.notin_(prevQuestions)).all()
            else:
                if prevQuestions is None:
                    questions = Question.query.filter(Question.category == category_id).all()         
                else:        
                    questions = Question.query.filter(Question.category == category_id).filter(Question.id.notin_(prevQuestions)).all()
            index = random.randint(0, len(questions)-1)
            random_question = questions[index]
            return jsonify({
                'success':True,
                'question':random_question.format()
                })
        except:
            abort(422)



    return app