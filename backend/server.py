
from flask import Flask
from project import app


@app.route('/')
def index():
    return '<h1>Hello Flask! </h1>'


if __name__ == '__main__':
    app.run(ssl_context='adhoc',host='0.0.0.0', port=5000) 