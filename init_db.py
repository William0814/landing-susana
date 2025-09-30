from dotenv import load_dotenv
load_dotenv()

from percistence.form import db
from app import app

with app.app_context():
    db.create_all()
    print("Tabla 'form' creada exitosamente en MySQL.")