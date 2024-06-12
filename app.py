import logging
from flask import Flask
from config import Config
from models import db
from routes import main

app = Flask(__name__)
app.config.from_object(Config)

# Configuración del logger
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
