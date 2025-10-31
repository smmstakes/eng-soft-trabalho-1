from flask import Flask
#from app.routes.projeto_routes import projeto_bp

app = Flask(__name__)


@app.route("/")
def home():
    return "Servidor está no ar"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)