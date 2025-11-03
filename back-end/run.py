from flask import Flask
from app.routes.projeto_routes import projeto_bp
from app.models.connection import db_path, engine, metadata

def create_app():

    app = Flask(__name__)
    app.register_blueprint(projeto_bp)
            
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)