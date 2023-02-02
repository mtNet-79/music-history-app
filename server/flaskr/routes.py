from flask import Flask, request, abort, jsonify
from flask_cors import CORS
# from flask import current_app
from models import Question, Category
# from flaskr import app
from flask import Blueprint
import random
from random import choice

main = Blueprint('main', __name__)


QUESTIONS_PER_PAGE = 10


def paginate_results(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [q.format() for q in selection]
    current_questions = questions[start:end]

    return current_questions


def create_dict(arr):
    cats_dict = {}
    for x in arr:
        k = list(x.items())[0][1]
        v = list(x.items())[1][1]
        cats_dict[k] = v
    return cats_dict


# IMPLEMENT CROSS-ORIGIN RESOURCE SHARING FOR ALL ORIGINS
CORS(main, origins=["*"])


@main.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response

#----------------------------HOME PAGE ROUTES-----------------------------------------#


@main.route("/questions")
def get_questions():
    sltcn = Question.query.order_by(Question.id).all()
    current_slctn = paginate_results(request, sltcn)
    cats = Category.query.all()

    formatted_cats = [cat.format() for cat in cats]
    cats_dict = create_dict(formatted_cats)
    if len(current_slctn) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "questions": current_slctn,
            "total_questions": len(Question.query.all()),
            "current_category": 'all',
            "categories": cats_dict
        }
    )


@main.route('/categories/<int:cat_id>/questions')
def get_questions_by_category(cat_id):
    try:
        cat = Category.query.filter(Category.id == cat_id).one_or_none()

        questions = Question.query.filter(Question.category_id == cat_id).all()

        curr_questions = paginate_results(request, questions)

        return jsonify({
            'success': True,
            'questions': curr_questions,
            'total_questions': len(questions),
            'current_category': cat.type
        })
    except:
        abort(404)


@main.route("/questions", methods=['POST'])
def search_question_by_term():
    body = request.get_json()

    search_term = body.get('searchTerm', None)

    try:
        questions = Question.query.filter(
            Question.question.like(f"%{search_term}%")).all()

        pagedQueryRes = paginate_results(request, questions)

        return jsonify({
            'success': True,
            'questions': pagedQueryRes,
            'totalQuestions': len(questions)
        })

    except:
        abort(500)


@main.route("/questions/<int:qid>", methods=['DELETE'])
def delete_question(qid):
    question = Question.query.filter(Question.id == qid).one_or_none()
    if question is None:
        abort(404)

    question.delete()
    slctn = Question.query.order_by(Question.id).all()
    curr_questions = paginate_results(request, slctn)

    return jsonify({
        'success': True,
        'deleted': qid,
        'questions': curr_questions,
        'total_questions': len(slctn)
    })

#----------------------ADD PAGE-------------------------------#


@main.route("/categories")
def get_all_categories():
    cats = Category.query.order_by(Category.id).all()
    formatted_categories = [cat.format() for cat in cats]
    cats_dict = create_dict(formatted_categories)

    if len(cats) == 0:
        abort(500)
    return jsonify({
        "success": True,
        "categories": cats_dict
    })


@main.route("/add", methods=['POST'])
def create_question():
    try:
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')
        setID = body.get('id', None)

        if setID:
            question = Question(
                question=new_question,
                answer=new_answer,
                category_id=category,
                difficulty=difficulty,
                id=setID
            )
        else:            
            question = Question(
                question=new_question,
                answer=new_answer,
                category_id=category,
                difficulty=difficulty
            )

        question.insert()

        slctn = Question.query.order_by(Question.id).all()
        current_slctn = paginate_results(request, slctn)

        return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_slctn,
            'total_questions': len(slctn)
        })
    except:
        abort(405)


@main.route("/questions/<int:question_id>")
def get_question(question_id):

    question = Question.query.get(question_id)

    formatted_question = question.format()

    return jsonify({
        'success': True,
        'question': formatted_question
    })


@main.route('/quizzes', methods=['POST'])
def play_quiz():
    body = request.get_json()

    previous_questions_ids = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)
    category = quiz_category['type']
    questions = Question.query.all()

    if quiz_category['type'] != "All":
        questions = Question.query.filter(
            Question.category_id == quiz_category['id']).all()

    if questions:
        rand_index_num = random.randrange(len(questions))
    else:
        return jsonify({
            'success': True,
            'currentQuestion': None
        })
    rtrnObj = {}
    current_question = None

    if len(previous_questions_ids) > 0:
        prevRange = []
        while questions[rand_index_num].id in previous_questions_ids:
            prevRange.append(rand_index_num)
            qsAvailable = [i for i in range(
                len(questions)) if i not in prevRange]
            if qsAvailable:
                rand_index_num = choice(qsAvailable)
            else:
                break
        else:
            current_question = questions[rand_index_num]
    else:
        current_question = questions[rand_index_num]
    if not current_question:
        rtrnObj = {
            'success': True,
            'currentQuestion': None
        }
    else:
        rtrnObj = {
            'success': True,
            'currentQuestion': current_question.format(),
        }
    return jsonify(rtrnObj)


@main.errorhandler(400)
def bad_request(error):
    return (
        jsonify({"success": False, "error": 400,
                "message": "Bad request"}),
        400,
    )


@main.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404,
                "message": "resource not found"}),
        404,
    )


@main.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify({"success": False, "error": 405,
                "message": "method not allowed"}),
        405,
    )


@main.errorhandler(422)
def unproccessable_entity(error):
    return (
        jsonify({"success": False, "error": 422,
                "message": "unproccessable entity"}),
        422,
    )


@main.errorhandler(500)
def unproccessable_entity(error):
    return (
        jsonify({"success": False, "error": 500,
                "message": "server error"}),
        422,
    )