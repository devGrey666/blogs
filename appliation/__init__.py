from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from application.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login.login_manager import LoginManager

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    # Initializing apps instances
    mail.__init__(app)
    db.__init__(app=app, session_options={'autoflush': False,'autocommit':False,'expire_on_commit':False})
    bcrypt.__init__(app)
    login_manager.__init__(app)
    from application.error.errorHandlers import errors
    from application.main.views import main
    from application.users.views import users
    from application.authors.views import authors
    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(authors)

    return app

# if app.config["ENV"] == 'production':
#     app.config.from_object("config.ProductionConfig")
# elif app.config["ENV"] == "development":
#     app.config.from_object("config.DevelopmentConfig")
# else:
#     app.config.from_object("config.TestingConfig")
