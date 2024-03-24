from flask import Flask, send_file, make_response, render_template
from flask_cors import CORS, cross_origin
from pytube import YouTube, Channel
import os
import ffmpeg

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

@app.get('/video/<video_id>')
@cross_origin(origins='http://localhost:5173')
def get_video(video_id):
    try:
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        ch = Channel(yt.channel_url)
    except:
        return {
            'error': 'Invalid URL'
        }
    return {
        'title': yt.title,
        'thumbnail': yt.thumbnail_url,
        'channelName': ch.channel_name,
        'views': yt.views,
        'video_id': video_id,
    }

@app.post('/video/<video_id>')
@cross_origin(origins='http://localhost:5173')
def post_video(video_id):
    filename = download_audio(video_id)
    response = make_response(send_file(filename, as_attachment=True))
    response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response

@app.get('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)