from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

def download_video(video_url):
    yt = YouTube(video_url)
    stream = yt.streams.filter(file_extension='mp4').first()
    stream.download(filename='video.mp4')
    return 'video.mp4'

def download_audio(video_url):
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename='audio.mp3')
    return 'audio.mp3'

def download_subtitles(video_url):
    yt = YouTube(video_url)
    caption = yt.captions.get_by_language_code('en')
    if caption:
        srt = caption.generate_srt_captions()
        with open('subtitles.srt', 'w') as f:
            f.write(srt)
        return 'subtitles.srt'
    return None

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data['url']
    
    video_path = download_video(video_url)
    audio_path = download_audio(video_url)
    subtitles_path = download_subtitles(video_url)
    
    response = {
        'video': video_path,
        'audio': audio_path,
        'subtitles': subtitles_path if subtitles_path else 'No subtitles available'
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
