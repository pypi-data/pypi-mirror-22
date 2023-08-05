Flask-bluelogin
===============

Flask-bluelogin provides user session management for Flask by blueprint component

It use flask-login module

Installation
------------

::

    pip install flask-bluelogin
        
Or

::

    git clone https://github.com/fraoustin/flask-bluelogin.git
    cd flask-bluelogin
    python setup.py install

Usage
-----

::

    from flask import Flask, request, current_app
    from flask_bluelogin import BlueLogin, User, Users, check_login
    import logging

    app = Flask(__name__)
    app.secret_key = 'super secret string'
    app.register_blueprint(BlueLogin(url_prefix="/api", ui_testing=True))
    User(id="fred", password="fred").save()
    Users().add_user(User(id='admin', password='passadmin', groups=['admin',]))
    Users().add_user(User(id='test', password='passtest'))

    @app.route("/")
    def hello():
        return "Hello World!"

    @app.route("/check")
    @check_login()
    def check():
        return "You are authentified"

    @app.route("/admin")
    @check_login("admin")
    def admin():
        return "you are admin"


    if __name__ == "__main__":
        app.run(port=8080)   #TODO



You can use BlueLogin.add_check_login for add control login on endpoint
