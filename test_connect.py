from models import db
from config import Config
from flask import Flask
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM organizations LIMIT 1"))  # 替换为你要测试的表名
            data = [dict(row._mapping) for row in result]
            print("Database connection successful!")
            print("Data:", data)

    except Exception as e:
        print(f"Database connection error: {e}")
