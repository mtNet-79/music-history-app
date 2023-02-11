from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
# from flask import current_app
from models import Composer
# from flaskr import app
from flask import Blueprint
import random
from random import choice

main = Blueprint('main', __name__)


ITEMS_PER_PAGE = 10


def paginate_results(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [i.format() for i in selection]
    current_items = items[start:end]

    return current_items


def create_dict(arr):
    cats_dict = {}
    for x in arr:
        k = list(x.items())[0][1]
        v = list(x.items())[1][1]
        cats_dict[k] = v
    return cats_dict


# IMPLEMENT CROSS-ORIGIN RESOURCE SHARING FOR ALL ORIGINS
# CORS(main, origins=["*"])
CORS(main, resources={r"/api/*": {"origins": "*"}})


@main.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response

# ----------------------------HOME PAGE ROUTES-----------------------------------------#


@main.route("/composers")
@cross_origin()
def get_composers():
    sltcn = Composer.query.order_by(Composer.id).all()
    print(f"get slctn {sltcn}")
    current_slctn = paginate_results(request, sltcn)
    print(f"get current_slctn {current_slctn}")
    # cats = Category.query.all()

    # formatted_cats = [cat.format() for cat in cats]
    # cats_dict = create_dict(formatted_cats)
    if len(current_slctn) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "composers": current_slctn,
            "total_composers": len(sltcn),
            "current_category": 'all'
            # "categories": cats_dict
        }
    )


@main.route("/composers/create", methods=['POST'])
def create_composer():
    # try:
    body = request.get_json()

    composer_name = body.get('name')
    years = body.get('years')
    nationality = body.get('nationality')
    setID = body.get('id', None)

    if setID:
        composer = Composer(
            name=composer_name,
            years=years,
            nationality=nationality,
            id=setID
        )
    else:
        composer = Composer(
            name=composer_name,
            years=years,
            nationality=nationality
        )

    composer.insert()

    slctn = Composer.query.order_by(Composer.id).all()
    current_slctn = paginate_results(request, slctn)

    return jsonify({
        'success': True,
        'created': composer.id,
        'composers': current_slctn,
        'total_Composers': len(slctn)
    })
    # except:
    #     abort(405)


@main.route("/composers/<int:composer_id>")
def get_Composer(composer_id):
    # print(f"composer id {composer_id}")
    composer = Composer.query.get(composer_id)

    formatted_composer = composer.format()

    return jsonify({
        'success': True,
        'composer': formatted_composer
    })
# @main.route('/categories/<int:cat_id>/Composers')
# def get_Composers_by_category(cat_id):
#     try:
#         cat = Category.query.filter(Category.id == cat_id).one_or_none()

#         Composers = Composer.query.filter(Composer.category_id == cat_id).all()

#         curr_Composers = paginate_results(request, Composers)

#         return jsonify({
#             'success': True,
#             'Composers': curr_Composers,
#             'total_Composers': len(Composers),
#             'current_category': cat.type
#         })
#     except:
#         abort(404)


# @main.route("/composers/create", methods=['POST'])
# def search_Composer_by_term():
#     body = request.get_json()

#     search_term = body.get('searchTerm', None)

#     try:
#         Composers = Composer.query.filter(
#             Composer.Composer.like(f"%{search_term}%")).all()

#         pagedQueryRes = paginate_results(request, Composers)

#         return jsonify({
#             'success': True,
#             'Composers': pagedQueryRes,
#             'totalComposers': len(Composers)
#         })

#     except:
#         abort(500)


@main.route("/composers/<int:qid>", methods=['DELETE'])
def delete_Composer(qid):
    composer = Composer.query.filter(Composer.id == qid).one_or_none()
    if composer is None:
        abort(404)

    composer.delete()
    slctn = Composer.query.order_by(Composer.id).all()
    curr_composers = paginate_results(request, slctn)

    return jsonify({
        'success': True,
        'deleted': qid,
        'Composers': curr_composers,
        'total_Composers': len(slctn)
    })

# ----------------------ADD PAGE-------------------------------#


# @main.route("/categories")
# def get_all_categories():
#     cats = Category.query.order_by(Category.id).all()
#     formatted_categories = [cat.format() for cat in cats]
#     cats_dict = create_dict(formatted_categories)

#     if len(cats) == 0:
#         abort(500)
#     return jsonify({
#         "success": True,
#         "categories": cats_dict
#     })


# @main.route('/quizzes', methods=['POST'])
# def play_quiz():
#     body = request.get_json()

#     previous_Composers_ids = body.get('previous_Composers', None)
#     quiz_category = body.get('quiz_category', None)
#     category = quiz_category['type']
#     Composers = Composer.query.all()

#     if quiz_category['type'] != "All":
#         Composers = Composer.query.filter(
#             Composer.category_id == quiz_category['id']).all()

#     if Composers:
    #     rand_index_num = random.randrange(len(Composers))
    # else:
    #     return jsonify({
    #         'success': True,
    #         'currentComposer': None
    #     })
    # rtrnObj = {}
    # current_Composer = None

    # if len(previous_Composers_ids) > 0:
    #     prevRange = []
    #     while Composers[rand_index_num].id in previous_Composers_ids:
    #         prevRange.append(rand_index_num)
    #         qsAvailable = [i for i in range(
    #             len(Composers)) if i not in prevRange]
    #         if qsAvailable:
    #             rand_index_num = choice(qsAvailable)
    #         else:
    #             break
    #     else:
    #         current_Composer = Composers[rand_index_num]
    # else:
    #     current_Composer = Composers[rand_index_num]
    # if not current_Composer:
    #     rtrnObj = {
    #         'success': True,
    #         'currentComposer': None
    #     }
    # else:
    #     rtrnObj = {
    #         'success': True,
    #         'currentComposer': current_Composer.format(),
    #     }
    # return jsonify(rtrnObj)


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
