import os

from flask import Flask, jsonify
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    # app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")
    CORS(app)

    # app.config['SECRET_KEY'] = '12345_QBMS'
    app.config.from_mapping(
        SECRET_KEY='12345_QBMS',
        DEBUG = True,
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # @app.route('/', methods=['GET'])
    # def ping_pong():
    #     return jsonify(app.static_folder)

    from flaskr import db
    db.init_app(app)

    from flaskr import api_auth, api_get, api_upload
    app.register_blueprint(api_auth.bp)
    app.register_blueprint(api_get.bp)
    app.register_blueprint(api_upload.bp)

    return app