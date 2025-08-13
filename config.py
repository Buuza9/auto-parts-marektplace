import os

# Base directory for the dotenv file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "your_secret_key_here"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False