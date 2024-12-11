from flask import Flask, render_template, request, redirect, url_for
import os
import logging
from pydub import AudioSegment
from pydub.playback import play
from transcribe import audio_to_text_whisper
from summarize import summarize_text

app = Flask(__name__)

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Set path FFmpeg untuk pydub
ffmpeg_path = r"D:/py/ffmpeg/bin"
AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")
os.environ["PATH"] += os.pathsep + ffmpeg_path

# Membuat folder uploads jika belum ada
upload_folder = 'uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Mendapatkan file audio dari form
        audio_file = request.files['audio_file']
        
        # Menentukan path untuk menyimpan file yang diunggah
        file_path = os.path.join(upload_folder, audio_file.filename)
        audio_file.save(file_path)

        # Proses audio
        result = process_audio(file_path)
        
        # Mengembalikan hasil ke halaman index.html
        return render_template('index.html', result=result, audio_file=audio_file.filename)
    
    return render_template('index.html')

def process_audio(input_audio):
    logging.info(f"Processing audio file: {input_audio}")

    result = {}

    # Periksa apakah file input ada
    if not os.path.exists(input_audio):
        logging.error(f"Audio file not found: {input_audio}")
        result["error"] = f"Audio file not found: {input_audio}"
    else:
        # Transkripsi MP3 ke teks menggunakan Whisper
        transcribed_text = audio_to_text_whisper(input_audio)

        if "Error" not in transcribed_text:
            logging.info("Transcription successful.")
            result["transcribed_text"] = transcribed_text

            # Ringkasan teks
            summarized_text = summarize_text(transcribed_text)
            if "Error" not in summarized_text:
                result["summarized_text"] = summarized_text
            else:
                logging.error(summarized_text)
                result["error"] = summarized_text
        else:
            logging.error(transcribed_text)
            result["error"] = transcribed_text

        # Informasi tentang file audio
        try:
            audio = AudioSegment.from_file(input_audio)
            result["audio_duration"] = f"{len(audio) / 1000} seconds"
            result["audio_sample_rate"] = f"{audio.frame_rate} Hz"
            result["audio_channels"] = f"{audio.channels}"

            # (Opsional) Putar audio untuk memverifikasi
            logging.info("Playing audio...")
            play(audio)
        except Exception as e:
            logging.error(f"Error processing audio file: {e}")
            result["error"] = f"Error processing audio file: {e}"

    return result

if __name__ == '__main__':
    app.run(debug=True)
