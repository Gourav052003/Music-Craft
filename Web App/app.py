from flask import (Flask, render_template, request,
send_from_directory,redirect,url_for,send_file,jsonify)
import os
from pathlib import Path
from threading import Thread
from flask_ngrok2 import run_with_ngrok

import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

model = MusicGen.get_pretrained('melody')
model.set_generation_params(duration=8)
descriptions = ['happy rock', 'energetic EDM', 'sad jazz']

app = Flask(__name__)
run_with_ngrok(app = app,auth_token = 'ngrok_auth_token') # if running it on google colab

MUSIC_PATH = Path('/Web App/audio data/Music')
DOWNLOADS_PATH = Path('/Web App/audio data/downloads')

os.makedirs(MUSIC_PATH,exist_ok=True)
os.makedirs(DOWNLOADS_PATH,exist_ok=True)

progress_percent = 0

@app.route('/')
def index():
    return render_template('landing_page.html')

@app.route('/<filename>')
def play_audio(filename):
    return send_from_directory(MUSIC_PATH, filename)

@app.route('/loader', methods=['POST'])
def loader():
    return jsonify({'status': 'success'})

@app.route('/<filename>')
def download_audio(filename):
    temp_filename = filename.split('.wav')[0]
    download_directory = os.path.join(DOWNLOADS_PATH,temp_filename)
    download_path = os.path.join(download_directory,filename)
    return send_file(download_path, as_attachment=True, download_name=filename)

@app.route('/<folder>/<filename>')
def play_audio_results(folder,filename):
    result_path = os.path.join(DOWNLOADS_PATH,folder)
    return send_from_directory(result_path,filename)

@app.route('/linking/<filename>')
def link_to_file(filename):
    return render_template(filename)


@app.route('/upload', methods=['POST'])
def upload():
    global progress_percent
    progress_percent = 5

    if 'AudioFile' in request.files:
        audio_file = request.files['AudioFile']
        progress_percent = 10

        if audio_file:
            filename = os.path.join(MUSIC_PATH,audio_file.filename)
            audio_file.save(filename)
            progress_percent = 25

            melody, sr = torchaudio.load(filename)
            wav = model.generate_with_chroma(descriptions, melody[None].expand(3, -1, -1), sr)
            progress_percent = 60


            os.chdir(DOWNLOADS_PATH)
            directory_name = audio_file.filename.split('.mp3')[0]
            progress_percent = 65

            os.makedirs(directory_name,exist_ok=True)
            os.chdir(directory_name)
            progress_percent = 75

            for idx, one_wav in enumerate(wav):
                audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness")

            progress_percent = 85

            os.chdir('/Web App')

            progress_percent = 95

            folder_name = audio_file.filename.split('.mp3')[0]

            progress_percent = 100

            return render_template('Music_app.html',
                                    filename = url_for('play_audio',filename = audio_file.filename),
                                    wav0_filename = url_for('play_audio_results',folder = folder_name,filename ='0.wav'),
                                    wav1_filename = url_for('play_audio_results',folder = folder_name,filename ='1.wav'),
                                    wav2_filename = url_for('play_audio_results',folder = folder_name,filename ='2.wav')
                                    )

    progress_percent = 100
    return "File not uploaded"



@app.route('/start_function')
def start_function():
    task_thread = Thread(target=upload)
    task_thread.start()
    return 'Function started'

@app.route('/get_progress')
def get_progress():
    progress = {'percent': progress_percent}
    return jsonify(progress)


app.run()