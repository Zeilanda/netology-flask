from flask import Flask
from cachetools import cached


@cached({})
def get_app():
    app = Flask('app')

    return app
