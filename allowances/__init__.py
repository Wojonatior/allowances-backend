import os
from .api import app, db

if not os.path.exists('db.sqlite'):
    db.create_all()
