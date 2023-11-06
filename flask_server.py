from flask import Flask, request, response
from werkzeug.utils import secure_filename
import yt_dlp

app = Flask(__name__)

@app.route('/image/saveImage', methods = ['GET', 'POST'])
def saveImage():
    if request.method == 'POST':
        img = request.files['file']
        img.save('static/image/' + secure_filename(img.filename))
        return 'static/image/' + secure_filename(img.filename)

@app.route('/video/saveVideo', methods = ['GET', 'POST'])
def saveVideo():
    if request.method == 'POST':
        vid = request.files['file']
        vid.save('static/video/' + secure_filename(vid.filename))
        return 'static/video/' + secure_filename(vid.filename)

@app.route('/video/YouTubeVideo', methods = ['GET', 'POST'])
def saveYouTube():
    if request.method == 'POST':
        url = request.form['youtube_url']
        ydl_opts = {
        'format': 'best',
        'outtmpl': 'static/video/%(id)s.mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return 'static/video/%(id)s.mp4'


@app.route('/record/saveRecord', methods = ['GET', 'POST'])
def saveRecord():
    if request.method == 'POST':
        rec = request.files['file']
        rec.save('static/record/' + secure_filename(rec.filename))
        return 'static/record/' + secure_filename(rec.filename)
    

if __name__ == '__main__':
    app.run(debug=True)