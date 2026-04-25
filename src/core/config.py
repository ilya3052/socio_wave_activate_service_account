import os

from dotenv import load_dotenv

load_dotenv('src/core/cfg/.env')

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
KEY = os.getenv('ENCRYPTION_KEY')
SESSION_FOLDER = os.getenv('SESSIONS_FOLDER')
