from flask import Flask, request
from werkzeug.utils import secure_filename
import yt_dlp
import os

app = Flask(__name__)

@app.route('/image/saveImage', methods = ['GET', 'POST'])
def saveImage():
    if request.method == 'POST':
        img = request.files['img']
        name, extension = os.path.splitext(img.filename)
        extension = '.png'
        img.save('static/image/' + secure_filename(name) + extension)
        return 'static/image/' + secure_filename(name) + extension

@app.route('/video/saveVideo', methods = ['GET', 'POST'])
def saveVideo():
    if request.method == 'POST':
        vid = request.files['vid']
        name, extension = os.path.splitext(vid.filename)
        extension = '.mp4'
        vid.save('static/video/' + secure_filename(name) + extension)
        return 'static/video/' + secure_filename(name) + extension

@app.route('/video/YouTubeVideo', methods = ['GET', 'POST'])
def saveYouTube():
    if request.method == 'POST':
        url = request.form['url']
        ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': 'static/video/%(id)s.mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return 'static/video/%(id)s.mp4'


@app.route('/record/saveRecord', methods = ['GET', 'POST'])
def saveRecord():
    if request.method == 'POST':
        rec = request.files['rec']
        name, extension = os.path.splitext(rec.filename)
        extension = '.m4a'
        rec.save('static/record/' + secure_filename(name)) + extension
        return 'static/record/' + secure_filename(name) + extension
    

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)