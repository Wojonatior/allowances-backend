import os
import datetime
import plaid
from flask import Flask, abort, request, render_template, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_graphql import GraphQLView
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy.ext.declarative import declarative_base
from schema import schema

app = Flask(__name__)

app.config.from_pyfile('.config')
PLAID_CLIENT_ID = app.config['PLAID_CLIENT_ID']
PLAID_SECRET = app.config['PLAID_SECRET']
PLAID_PUBLIC_KEY = app.config['PLAID_PUBLIC_KEY']
PLAID_ENV = app.config['PLAID_ENV']

# extensions
auth = HTTPBasicAuth()
client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                      public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
access_token = None
public_token = None

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route("/")
def index():
    return render_template('index.ejs', plaid_public_key=PLAID_PUBLIC_KEY, plaid_environment=PLAID_ENV)


@app.route("/get_access_token", methods=['POST'])
def get_access_token():
    global access_token
    public_token = request.form['public_token']
    exchange_response = client.Item.public_token.exchange(public_token)
    access_token = exchange_response['access_token']

    return jsonify(exchange_response)


@app.route("/accounts", methods=['GET'])
def accounts():
    global access_token
    accounts = client.Auth.get(access_token)
    return jsonify(accounts)


@app.route("/item", methods=['GET', 'POST'])
def item():
    global access_token
    item_response = client.Item.get(access_token)
    institution_response = client.Institutions.get_by_id(
        item_response['item']['institution_id'])
    return jsonify({'item': item_response['item'], 'institution': institution_response['institution']})


@app.route("/transactions", methods=['GET', 'POST'])
def transactions():
    global access_token
    # Pull transactions for the last 30 days
    start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() +
                                      datetime.timedelta(-30))
    end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())

    try:
        response = client.Transactions.get(access_token, start_date, end_date)
        return jsonify(response)
    except plaid.errors.PlaidError as e:
        return jsonify({'error': {'error_code': e.code, 'error_message': str(e)}})


@app.route("/create_public_token", methods=['GET'])
def create_public_token():
    global access_token
    response = client.Item.public_token.create(access_token)
    return jsonify(response)


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})



if(__name__ == '__main__'):
    app.run(debug=True)
