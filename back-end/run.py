from flask import Flask
from app.routes.projeto_routes import projeto_bp
from app.routes.user_story_routes import user_story_bp
from app.routes.sprint_routes import sprint_bp
from app.routes.task_routes import task_bp
from app.models.connection import db_path, engine, metadata
from flask_cors import CORS

def create_app():

    app = Flask(__name__)
    
    CORS(app)
    
    # TODO: Deploy -> Isso não pode ficar exposto aqui usalmente. Precisa estar num .env
    CORS(app, origins="http://localhost:3000")
    
    app.register_blueprint(projeto_bp)
    app.register_blueprint(user_story_bp)
    app.register_blueprint(sprint_bp)
    app.register_blueprint(task_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)