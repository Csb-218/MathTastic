import os
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

cred_json = {
  "type": os.getenv("TYPE"),
  "project_id": os.getenv("PROJECT_ID"),
  "private_key_id": os.getenv("PRIVATE_KEY_ID"),
  "private_key": os.getenv("PRIVATE_KEY"),
  "client_email": os.getenv("CLIENT_EMAIL"),
  "client_id": os.getenv("CLIENT_ID"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
  "universe_domain": "googleapis.com"
}

# Initialize Firebase Admin with service account
cred = credentials.Certificate(cred_json)

# Initialize the app
default_app = firebase_admin.initialize_app(cred)

# Get auth instance
auth_instance = auth.Client(default_app)