import os

import connexion
from flask import Flask, abort, make_response, render_template, redirect

from shepherd.exceptions import EmptyOrderException, NegativeValueException


def error_handling(app):
    @app.errorhandler(EmptyOrderException)
    def handle_empty_order_exception(ex):
        return 'Order should not be empty', 400

    @app.errorhandler(NegativeValueException)
    def handle_negative_value_exception(ex):
        return 'Order should not contain negative values', 400


def create_app(test_config=None):
    # create and configure the app
    app = connexion.App(__name__, specification_dir="./", server_args={'instance_relative_config': True})
    app.app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.app.instance_path, 'shepherd.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return redirect('/overview')

    @app.route('/overview')
    def overview():
        return render_template('overview.html')

    @app.route('/healthcheck')
    def healthcheck():
        return 'Ok'

    # Read the swagger.yml file to configure the endpoints
    app.add_api("swagger.yml", strict_validation=True)

    error_handling(app.app)

    from shepherd import db
    db.init_app(app.app)

    return app.app
