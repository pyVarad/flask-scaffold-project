import os
from app import create_app
from db import db


app_config = os.getenv('APP_CONFIG', 'config/dev.toml')
app = create_app(app_config)

@app.before_first_request
def create_db():
    db.create_all()

db.init_app(app)
app.run(host="0.0.0.0", port=5000, debug=True)