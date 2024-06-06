from flask import Flask, send_file, make_response, render_template
from flask_cors import CORS
from pytube import YouTube, Channel, Playlist
import os, re
import ffmpeg
from typing import List

app = Flask(__name__,
            static_folder='../ui/dist',
            static_url_path='/',
            template_folder='../ui/dist')

CORS(app)

def download_audio(video_id):
    audio = YouTube(f'https://www.youtube.com/watch?v={video_id}').streams.filter(only_audio=True, audio_codec='opus').desc().first()
            
    # get the default filename for the video
    default_filename = f'tmp/{audio.default_filename.replace(".webm", ".mp3")}'

    # good service (.webm) => (.mp3) for FREE!
    # TODO: Make this non-blocking and allow overwrites
    audio.download(output_path='tmp', filename='tmp.webm')
    ffmpeg.input('tmp/tmp.webm').output(default_filename).run(quiet=True, overwrite_output=True)
    
    # remove this tmp menace
    os.remove('tmp/tmp.webm')
    return default_filename

def videoFlow(video_id):
    try:
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        ch = Channel(yt.channel_url)
    except:
        return {
            'error': 'Invalid Video URL'
        }
    return {
        'title': yt.title,
        'thumbnail': yt.thumbnail_url,
        'channelName': ch.channel_name,
        'views': yt.views,
        'video_id': video_id,
    }

def playlistFlow(list_id):
    try:
        pl = Playlist(f'https://www.youtube.com/playlist?list={list_id}')
        return [ videoFlow(v.video_id) for v in pl.videos ]
    except:
        return {
            'error': 'Invalid Playlist URL'
        }

@app.get('/video/<path:link>')
def get_video(link) -> List:
    VID_URL_PATTERN = '\/watch\?v=(.+)'
    LIST_URL_PATTERN = '\/playlist\?list=(.+)'
    video_id = re.findall(VID_URL_PATTERN, link, re.S)
    if video_id:
        return [ videoFlow(video_id[0]) ]

    list_id = re.findall(LIST_URL_PATTERN, link, re.S)
    if list_id:
        return playlistFlow(list_id[0])
    
    return {
        'error': 'Invalid URL'
    }

@app.post('/video/<video_id>')
def post_video(video_id):
    filename = download_audio(video_id)
    response = make_response(send_file(filename, as_attachment=True))
    response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response

@app.get('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)