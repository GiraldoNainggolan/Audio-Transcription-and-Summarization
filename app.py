from flask import Flask, render_template, request
import os
import logging
import uuid
from pydub import AudioSegment
from pydub.playback import play
from transcribe import audio_to_text_whisper
from transformers import pipeline
from transformers import AutoTokenizer

app = Flask(__name__)

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Set path FFmpeg untuk pydub
ffmpeg_path = r"D:/py/ffmpeg/bin"
AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")
os.environ["PATH"] += os.pathsep + ffmpeg_path

# Membuat folder uploads jika belum ada
upload_folder = r'D:\py\uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# Konfigurasi pipeline summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Validasi file audio
        if 'audio_file' not in request.files:
            result = {"error": "No audio file part."}
            return render_template('index.html', result=result)

        audio_file = request.files['audio_file']
        if audio_file.filename == '':
            result = {"error": "No selected file."}
            return render_template('index.html', result=result)

        if not audio_file.filename.endswith('.mp3') and not audio_file.filename.endswith('.wav'):
            result = {"error": "File must be in MP3 or WAV format."}
            return render_template('index.html', result=result)

        # Menyimpan file dengan nama unik
        unique_filename = str(uuid.uuid4()) + os.path.splitext(audio_file.filename)[1]
        file_path = os.path.join(upload_folder, unique_filename)

        # Simpan file audio
        audio_file.save(file_path)

        # Proses audio
        result = process_audio(file_path)

        return render_template('index.html', result=result, audio_file=unique_filename)

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
            try:
                summarized_text = summarize_text(transcribed_text)
                result["summarized_text"] = summarized_text
            except Exception as e:
                logging.error(f"Error summarizing text: {e}")
                result["error"] = f"Error summarizing text: {e}"
        else:
            logging.error(transcribed_text)
            result["error"] = transcribed_text

        # Informasi tentang file audio
        try:
            audio = AudioSegment.from_file(input_audio)
            result["audio_duration"] = f"{len(audio) / 1000} seconds"
            result["audio_sample_rate"] = f"{audio.frame_rate} Hz"
            result["audio_channels"] = f"{audio.channels}"
        except Exception as e:
            logging.error(f"Error processing audio file: {e}")
            result["error"] = f"Error processing audio file: {e}"

    return result

def summarize_text(input_text):
    try:
        logging.info("Starting summarization...")
        if len(input_text.split()) < 10:
            raise ValueError("Text too short for summarization.")
        summary = summarizer(input_text, max_length=50, min_length=25, do_sample=False)
        logging.info("Summarization successful.")
        return summary[0]['summary_text']
    except ValueError as ve:
        logging.error(f"Error summarizing text: {ve}")
        return "Text too short to summarize."
    except Exception as e:
        logging.error(f"Unexpected error during summarization: {e}")
        return f"Error summarizing text: {e}"

if __name__ == '__main__':
    app.run(debug=True)
