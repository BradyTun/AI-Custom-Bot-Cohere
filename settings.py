import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
SQLALCHEMY_TRACK_MODIFICATIONS = False

