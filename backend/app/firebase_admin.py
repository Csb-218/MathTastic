import os
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase Admin with service account
cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

# Initialize the app
default_app = firebase_admin.initialize_app(cred)

# Get auth instance
auth_instance = auth.Client(default_app)