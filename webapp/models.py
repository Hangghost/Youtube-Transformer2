from . import db

# 定義資料庫的物件
class Video(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  views = db.Column(db.Integer)
  author = db.Column(db.String(255))    # 255表示字數上限
  video_title = db.Column(db.String(255))

  # 定義video object的初始值
  def __init__(self, views, author, video_title):
    self.views = views
    self.author = author
    self.video_title = video_title