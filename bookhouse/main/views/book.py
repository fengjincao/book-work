# -*- coding: utf-8 -*-

from flask import render_template, request, g, jsonify

from bookhouse.core import app, db
from bookhouse.main.misc.auth import auth_required
from bookhouse.models.book import Book


@app.route('/index/', methods=['GET'])
@app.route('/my/books/', methods=['GET'])
def books_page():
    return render_template('book_house.html')


@app.route('/api/books/', methods=['GET', 'POST'])
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
    elif request.method == 'POST':
        pass


@app.route('/api/books/<int:book_id>/', methods=['GET', 'PUT', 'DELETE'])
@auth_required
def book_api(book_id):
    if request.method == 'GET':
        pass

    elif request.method == 'PUT':
        pass

    elif request.method == 'DELETE':
        pass
