import Functions.crud as crud
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
