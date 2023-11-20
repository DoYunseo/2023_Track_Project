from flask import Flask, request
from werkzeug.utils import secure_filename
import yt_dlp
import os
import test

app = Flask(__name__)

if not (os.path.isdir('static')):
    os.makedirs('static')

@app.route('/image/saveImage', methods = ['GET', 'POST'])
def saveImage():
    if request.method == 'POST':
        img = request.files['img']
        name, extension = os.path.splitext(img.filename)
        extension = '.png'
        img.save('static/' + secure_filename('image') + extension)
        return 'static/' + secure_filename('image') + extension

@app.route('/video/saveVideo', methods = ['GET', 'POST'])
def saveVideo():
    if request.method == 'POST':
        vid = request.files['vid']
        name, extension = os.path.splitext(vid.filename)
        extension = '.mp4'
        vid.save('static/' + secure_filename('video') + extension)
        return 'static/' + secure_filename('video') + extension

@app.route('/video/YouTubeVideo', methods = ['GET', 'POST'])
def saveYouTube():
    if request.method == 'POST':
        url = request.form['url']
        ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': 'static/video.mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return 'static/video.mp4'


@app.route('/record/saveRecord', methods = ['GET', 'POST'])
def saveRecord():
    if request.method == 'POST':
        rec = request.files['rec']
        name, extension = os.path.splitext(rec.filename)
        extension = '.m4a'
        rec.save('static/' + secure_filename('record') + extension)
        return 'static/' + secure_filename('record') + extension
    
@app.route('/ai/getFile', methods=['GET'])
def getFile():
    path = 'static/'
    img_path = path + 'image.png'
    video_path = path + 'video.mp4'
    rec_path = path + 'record.m4a'
    if os.path.isfile(img_path) and os.path.isfile(video_path) and os.path.isfile(rec_path):
        return test.data_preprocessing(path)


@app.route('/ai/deleteImage', methods=['GET'])
def deleteImage():
    os.remove('static/image.png')
    return "Image deleted successfully"

@app.route('/ai/deleteVideo', methods=['GET'])
def deleteVideo():
    os.remove('static/video.mp4')
    return "Video deleted successfully"

@app.route('/ai/deleteRecord', methods=['GET'])
def deleteRecord():
    os.remove('static/record.m4a')
    return "record deleted successfully"

@app.route('/ai/deleteCover', methods=['GET'])
def deleteCover():
    os.remove('static/cover.mp4')
    return "covered video deleted successfully"

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
