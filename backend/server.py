
from flask import Flask
from project import app


@app.route('/')
def index():
    return '<h1>Hello Flask! </h1>'


if __name__ == '__main__':
    app.run(ssl_context=('/etc/letsencrypt/live/yourdomain.com/fullchain.pem',
                         '/etc/letsencrypt/live/yourdomain.com/privkey.pem'),
            port=5000) 