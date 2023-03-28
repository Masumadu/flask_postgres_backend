import os
import sys
from logging.config import dictConfig

from flask import Flask, jsonify, redirect
from flask.logging import default_handler
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy.exc import DBAPIError
from werkzeug.exceptions import HTTPException
from werkzeug.utils import import_string

# add app to system path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # noqa

# load dotenv in the base root
from app.api_spec import spec
from app.core.exceptions.app_exceptions import AppExceptionCase, app_exception_handler
from app.core.extensions import cors, db, healthcheck, ma, migrate
from app.health import HEALTH_CHECKS
from app.core.log_config import log_config

APP_ROOT = os.path.join(os.path.dirname(__file__), "..")  # refers to application_top

# configure log before creating application instance
dictConfig(log_config())

# SWAGGER
SWAGGER_URL = "/api/v1/resource/docs"
API_URL = "/static/swagger.json"

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Flask Backend Design For Enterprise Apps"}
)


def create_app(config="config.DevelopmentConfig"):
    """Construct the core application"""

    basedir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(basedir, "../instance")
    app = Flask(__name__, instance_relative_config=False, instance_path=path)

    app.logger.removeHandler(default_handler)
    with app.app_context():
        flask_debug = os.getenv("FLASK_DEBUG").lower()
        debug_mode = True if flask_debug in ["1", "true"] else False
        cfg = import_string(config)()
        if not debug_mode:
            print("loading production")
            cfg = import_string("config.ProductionConfig")()
        app.config.from_object(cfg)

        # add extensions
        register_extensions(app)
        register_blueprints(app)
        register_swagger_definitions(app)
        register_health_check(app)
        return app


def register_extensions(flask_app):
    """Register Flask extensions."""
    from app.core.factory import factory

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    ma.init_app(flask_app)
    factory.init_app(flask_app, db)
    cors.init_app(flask_app, resources={r"/api/*": {"origins": "*"}}, allow_headers="*")

    @flask_app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return app_exception_handler(e)

    @flask_app.errorhandler(DBAPIError)
    def handle_db_exception(e):
        return app_exception_handler(e)

    @flask_app.errorhandler(AppExceptionCase)
    def handle_app_exceptions(e):
        return app_exception_handler(e)

    return None


def register_blueprints(app):
    from .api.api_v1 import api

    """Register Flask blueprints."""
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    api.init_app(app)

    @app.route("/")
    def index():
        return redirect(SWAGGER_URL)

    return None


def register_swagger_definitions(app):
    with app.test_request_context():
        for fn_name in app.view_functions:
            if fn_name == "static":
                continue
            print(f"Loading swagger docs for function: {fn_name}")
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)

    @app.route("/static/swagger.json")
    def create_swagger_spec():
        """
        Swagger API definition.
        """
        return jsonify(spec.to_dict())


def register_health_check(app: Flask):
    for check in HEALTH_CHECKS:
        if callable(check):
            healthcheck.add_check(check)
    app.add_url_rule(
        "/api/v1/healthcheck", "healthcheck", view_func=lambda: healthcheck.run()
    )
    return None
