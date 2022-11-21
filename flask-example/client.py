from flask import Flask

from flask_example.blueprint import ClinicController 


def create_application() -> Flask:

    clinic = ClinicController()

    app = Flask(__name__)
    app.register_blueprint(clinic.blueprint)

    return app
