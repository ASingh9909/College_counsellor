# /api/index.py
# This file tells Vercel to use your existing Flask app from the backend folder.
from backend.app import app

# Vercel will look for an 'app' instance by default.
# If your Flask app instance in backend/app.py is named differently, adjust accordingly.