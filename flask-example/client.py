from flask import Flask

from flask_example.blueprint import ClinicController 


def create_application() -> Flask:

    app = Flask()
    app.add_url_rule('clinic', '/', ClinicController())

    return app
