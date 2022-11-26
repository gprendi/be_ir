from flask import Flask

def define_app():
    app = Flask(__name__)

    @app.get("/")
    def hello_world():
        return 'Hello World'

    @app.get("/hell")
    def hi():
        return "hi"

