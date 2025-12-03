# __init__.py
from flask import Flask
from config import Config
from extension import db, jwt, cors

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    print("SQLALCHEMY_DATABASE_URI =", app.config["SQLALCHEMY_DATABASE_URI"])


    db.init_app(app)
    jwt.init_app(app)

    cors.init_app(
        app,
        resources={r"/api/*": {"origins": [
            "http://localhost:3000",
            "http://127.0.0.1:5501"
        ]}},
        supports_credentials=True,
    )

    import models

    from routes import routes as routes_bp
    app.register_blueprint(routes_bp)

    return app
