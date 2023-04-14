from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 創一個新的SQLAlchemy object
db = SQLAlchemy()
YOUTUBE_DATABASE = "youtube_database.db"


def create_web_app():
  # 創造一個flask物件
  app = Flask(__name__)

  # 初始化資料庫
  app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{YOUTUBE_DATABASE}"
  db.init_app(app)

  # 註冊藍圖
  from .home import home
  app.register_blueprint(home, url_prefix="/")

  # 創建資料庫
  with app.app_context():
    db.create_all()
  
  return app

