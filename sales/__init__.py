import os
from flask import Flask
from .config import Config
from .models import db, migrate
from .rest import init_app
import logging

logging.basicConfig(filename='sales.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p'
                    )

def create_app(test_config=None):
    """create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'sales_test.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # init

    db.init_app(app)
    migrate.init_app(app, db)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/about')
    def hello():
        return 'This is pet project'

    init_app(app)

    return app
