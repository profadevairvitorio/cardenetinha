from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @app.context_processor
    def inject_year():
        return {'current_year': datetime.now().year}

    with app.app_context():
        from .routes.main_routes import main_bp
        from .routes.account_routes import account_bp
        from .routes.transaction_routes import transaction_bp
        from .routes.category_routes import category_bp
        from .routes.profile_routes import profile_bp
        from .routes.report_routes import report_bp
        from .routes.goal_routes import goal_bp
        from .routes.financial_planning_routes import financial_planning_bp
        from . import auth
        from . import models

        app.register_blueprint(main_bp)
        app.register_blueprint(account_bp)
        app.register_blueprint(transaction_bp)
        app.register_blueprint(category_bp)
        app.register_blueprint(profile_bp)
        app.register_blueprint(report_bp)
        app.register_blueprint(goal_bp)
        app.register_blueprint(financial_planning_bp)
        app.register_blueprint(auth.auth_bp)

    return app
