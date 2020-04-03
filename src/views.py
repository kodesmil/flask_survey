from flask import Blueprint, request, jsonify
from flask_apispec import marshal_with, doc
from kodesmil_common.auth import requires_auth
from kodesmil_common.user_schema import get_user
import os
import firebase_admin
from firebase_admin import auth

from . import db
from .models import AnswerSchema, QuestionSchema

content = Blueprint('content', __name__)
firebase_app = firebase_admin.initialize_app()

@doc(tags=['Answer'], description='')
@marshal_with(AnswerSchema())
@content.route('/answers', methods=['POST'])
def create_answer(*args, **kwargs):
    request_data = request.get_json()
    user = auth.get_user_by_email('hello@kodesmil.com')
    request_data['author_id'] = user.uid
    result = db.answers.insert_one(AnswerSchema().load(request_data))
    if result.acknowledged:
        return '', 201
    return '', 500


@doc(tags=['Answer'], description='')
@marshal_with(AnswerSchema())
@content.route('/answers', methods=['GET'])
def get_answers(*args, **kwargs):
    user = auth.get_user_by_email('hello@kodesmil.com')
    answers = db.answers \
        .find({'user_id': user.uid}) \
        .sort('_id', -1) \
        .limit(1)
    return jsonify(AnswerSchema().dump(
        answers, many=True
    )), 200


@doc(tags=['Question'], description='')
@marshal_with(QuestionSchema())
@content.route('/questions', methods=['GET'])
def get_questions(*args, **kwargs):
    return jsonify(QuestionSchema().dump(
        db.questions.find(), many=True,
    )), 200
