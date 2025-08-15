from flask import Flask
from .config import Config
from .extensions import db, ma, scheduler
from .routes.escrow_routes import escrow_bp
from flask_cors import CORS  # <-- Import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for all routes
    CORS(app)  # <-- Enable CORS

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    # Register blueprints
    app.register_blueprint(escrow_bp, url_prefix='/api/v1/escrow')

    # Health check route
    @app.route('/')
    def index():
        return 'Monero Escrow API is running!'

    return app