from flask import Blueprint, render_template, request, send_file, redirect, url_for
from pytube import YouTube
from .models import Video
from . import db

home = Blueprint("home", __name__)


@home.route("/", methods=["GET", "POST"])  # 路徑的原始狀態只能是GET，所以要用list
def download_youtube_video():
  # 訪問的時候是GET
  # 送出表個的時候是POST
  
  if request.method == "POST":
    # 把用戶在前端的網址取出來
    video_url = request.form.get("downloadUrl")
  
    # 用取出來的網址，創一個新的youtube物件
    youtube_video_object = YouTube(video_url)

    # 用物件內的功能取得觀看數、作者、影片名稱
    views = youtube_video_object.views
    author = youtube_video_object.author
    video_title = youtube_video_object.title

    # 寫入資料庫
    new_video = Video(views, author, video_title)
    db.session.add(new_video)    # session表示新增一個資料庫的執行
    db.session.commit()    # commit表示確定執行
  
    # 下載影片到伺服器
    get_video = youtube_video_object.streams.get_highest_resolution()

    
    # 讓用戶端下載，選擇存放路徑
    return send_file(get_video.download(), as_attachment=True)
    #redirect(url_for("home.download_youtube_video"))
  
  # 如果不是POST就執行GET
  else:
    # 讀取資料庫
    videos = Video.query.all()    # 在Video物件中查詢
    
    return render_template("home.html", videos=videos)

# 刪除功能
@home.route("/delete/<int:id>", methods=["POST"])
def delete_video(id):
  # 在資料庫中查詢要刪除的資料
  video = Video.query.filter_by(id=id).first()

  # 如果找到了要刪除的資料，就從資料庫中刪除
  if video:
    db.session.delete(video)
    db.session.commit()

  # 返回首頁
  return redirect(url_for("home.download_youtube_video"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
