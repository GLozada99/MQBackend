import Functions.crud as crud
import DB.classes as classes
import Functions.functions as func
from http import HTTPStatus
from flask import Flask, request, jsonify
from decouple import config
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config('FLASK_SECRET')
JWTManager(app)
CORS(app)


@app.route('/login', methods=['POST'])
def login():
    access_token = ''
    msg = 'Bad username or password'
    status = HTTPStatus.BAD_REQUEST

    data = request.get_json(force=True)
    if data:
        username = data.get('username')
        password = data.get('password')

        user = crud.get_user_by_username(username)
        if user and func.compare_hash(user.password, password):
            access_token = create_access_token(identity=username)
            msg = 'Welcome'
            status = HTTPStatus.OK

    return jsonify(msg=msg, access_token=access_token), status


@jwt_required
@app.route('/test', methods=['GET'])
def test():
    username = get_jwt_identity()
    return jsonify(msg=username)


@jwt_required
@app.route('/users', methods=['GET'])
def users():
    if request.method == 'GET':
        data = [elem.to_dict() for elem in crud.read(classes.User)]
        msg = '' if data else 'No entries'
        return jsonify(result=data, msg=msg), HTTPStatus.OK


@jwt_required
@app.route('/articles', methods=['GET'])
def articles():
    data = [elem.to_dict() for elem in crud.read(classes.Article)]
    msg = '' if data else 'No entries'
    return jsonify(result=data, msg=msg), HTTPStatus.OK


@jwt_required
@app.route('/clients', methods=['GET'])
def clients():
    data = [elem.to_dict() for elem in crud.read(classes.Client)]
    msg = '' if data else 'No entries'
    return jsonify(result=data, msg=msg), HTTPStatus.OK


@jwt_required
@app.route('/quotes', methods=['GET'])
def quotes():
    data = [elem.to_dict() for elem in crud.read(classes.Quote)]
    msg = '' if data else 'No entries'
    return jsonify(result=data, msg=msg), HTTPStatus.OK


@jwt_required
@app.route('/invoices', methods=['GET'])
def invoices():
    data = [elem.to_dict() for elem in crud.read(classes.Invoice)]
    msg = '' if data else 'No entries'
    return jsonify(result=data, msg=msg), HTTPStatus.OK


@jwt_required
@app.route('/users/<int:id_>', methods=['GET'])
def user_by_id(id_):
    data = crud.read(classes.Users, int(id_))
    status = HTTPStatus.NOT_FOUND
    if data:
        data = data.to_dict()
        msg = '' if data else 'No entry'
        status = HTTPStatus.OK
    return jsonify(result=data, msg=msg), status


@jwt_required
@app.route('/articles/<int:id_>', methods=['GET'])
def article_by_id(id_):
    data = crud.read(classes.Users, int(id_))
    status = HTTPStatus.NOT_FOUND
    if data:
        data = data.to_dict()
        msg = '' if data else 'No entry'
        status = HTTPStatus.OK
    return jsonify(result=data, msg=msg), status


@jwt_required
@app.route('/clients/<id>', methods=['GET'])
def client_by_id(id_):
    data = crud.read(classes.Users, int(id_))
    status = HTTPStatus.NOT_FOUND
    if data:
        data = data.to_dict()
        msg = '' if data else 'No entry'
        status = HTTPStatus.OK
    return jsonify(result=data, msg=msg), status


@jwt_required
@app.route('/quotes/<id>', methods=['GET'])
def quote_by_id(id_):
    data = crud.read(classes.Users, int(id_))
    status = HTTPStatus.NOT_FOUND
    if data:
        data = data.to_dict()
        msg = '' if data else 'No entry'
        status = HTTPStatus.OK
    return jsonify(result=data, msg=msg), status


@jwt_required
@app.route('/invoices/<id>', methods=['GET'])
def invoice_by_id(id_):
    data = crud.read(classes.Users, int(id_))
    status = HTTPStatus.NOT_FOUND
    if data:
        data = data.to_dict()
        msg = '' if data else 'No entry'
        status = HTTPStatus.OK
    return jsonify(result=data, msg=msg), status


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()

    ap.add_argument('--debug', action='store_true')
    args = vars(ap.parse_args())

    if args['debug']:
        app.run(host='0.0.0.0', debug=True)
    else:
        from gevent.pywsgi import WSGIServer
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
