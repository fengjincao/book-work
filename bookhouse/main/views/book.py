# -*- coding: utf-8 -*-

from flask import render_template, request, g, jsonify, abort
from cerberus import Validator
from bookhouse.core import app, db
from bookhouse.main.misc.auth import auth_required
from bookhouse.models.book import Book
from bookhouse.models.user import User


@app.route('/index/', methods=['GET'])
@app.route('/my/books/', methods=['GET'])
def books_page():
    return render_template('book_house.html')


@app.route('/api/books/', methods=['GET', 'PUT'])
@auth_required
def books_api():
    if request.method == 'GET':
        user = g.user
        items = Book.query.filter(db.text('user_id = :uid')).params(uid=user.id).all()
        resp_data = {
                        'status': 'success',
                        'data': {
                            'books': [{
                                'book_id': item.id,
                                'book_name': item.name,
                                'book_price': item.price,
                                'book_intro': item.intro,
                                'book_owner': user.name
                                } for item in items]
                        }
                    }
        return jsonify(**resp_data)
    elif request.method == 'PUT':
        request_data = request.json
        validator = Validator({
            'book_name': {
                'type': 'string',
                'minlength': 2,
                'maxlength': 30,
                'required': True,
            },
            'book_price': {
                'required': True,
            },
            "book_intro": {
                'type': 'string',
            },
        })
        if not validator.validate(request_data):
            resp_data = {
                'status': 'fail',
                'data': {
                    'code': 1,
                    'message': 'validate error',
                }
            }
            return jsonify(**resp_data)
        book = Book(
                name=request_data['book_name'],
                price=request_data['book_price'],
                intro=request_data['book_intro'],
                user_id=g.user.id
        )
        db.session.add(book)
        db.session.commit()
        return jsonify(**{})


@app.route('/api/books/<int:book_id>/', methods=['GET', 'POST', 'DELETE'])
@auth_required
def book_api(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(400)
    if request.method == 'GET':

        resp_data = {
            'book': {
                'book_id': book.id,
                'book_name': book.name,
                'book_intro': book.intro,
                'book_price': book.price,
                'book_owner': User.query.get(int(book.user_id)).name
            }
        }
        return jsonify(**resp_data)
    elif request.method == 'POST':
        request_data = request.json
        book.name = request_data['book_name']
        book.intro = request_data['book_intro']
        book.price = request_data['book_price']
        db.session.commit()
        return jsonify(**{})
    elif request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return jsonify(**{})

