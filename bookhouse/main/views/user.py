# -*- coding: utf-8 -*-

from cerberus import Validator
from flask import abort, jsonify, render_template, request

from bookhouse.core import app, db
from bookhouse.models.user import GENDER_OPTIONS, User
from bookhouse.main.misc.errors import ViewProcessJump
from bookhouse.main.views import API_FAIL_CODES


@app.route('/account/sign-up/', methods=['GET'])
def sign_up_page():
    return render_template('sign_up.html')


API_FAIL_CODES['SIGN_UP'] = {
    'USER_NAME_EXISTED': 1,
}


@app.route('/api/account/sign-up/', methods=['POST'])
def sign_up_api():
    if request.method == 'POST':
        try:
            request_data = request.json
            if request_data is None:
                raise ViewProcessJump(code='ILLEGAL_USER_INPUT')
            validator = Validator({
                'name': {
                    'required': True,
                    'type': 'string',
                    'maxlength': 16,
                },
                'password': {
                    'required': True,
                    'type': 'string',
                    'maxlength': 32,
                },
                'gender': {
                    'required': True,
                    'type': 'integer',
                    'allowed': GENDER_OPTIONS.values(),
                },
            })
            if not validator.validate(request_data):
                raise ViewProcessJump(code='ILLEGAL_USER_INPUT')

            name = validator.document.get('name')
            password = validator.document.get('password')
            gender = validator.document.get('gender')

            user_existed = User.query.filter(db.text('name = :name')).params(name=name).first()
            if user_existed:
                raise ViewProcessJump(code='USER_NAME_EXISTED')

            user = User()
            db.session.add(user)
            user.name = name
            user.password = password
            user.gender = gender

            db.session.commit()

            resp = {
                'status': 'success',
                'data': {
                    'token': str(user.id),
                    'name': user.name,
                },
            }

            return jsonify(**resp)

        except ViewProcessJump as e:
            if e.code in (
                    'ILLEGAL_USER_INPUT',
            ):
                abort(400)
            elif e.code in (
                    'USER_NAME_EXISTED',
            ):
                resp = {
                    'status': 'fail',
                    'data': {
                        'code': API_FAIL_CODES['SIGN_UP']['USER_NAME_EXISTED'],
                    },
                }
                return jsonify(**resp)
            else:
                assert False


@app.route('/', methods=['GET'])
@app.route('/account/sign-in/', methods=['GET'])
def sign_in_page():
    return render_template('sign_in.html')


@app.route('/api/account/sign-in/', methods=['POST'])
def sign_in_api():
    if request.method == 'POST':
        pass
