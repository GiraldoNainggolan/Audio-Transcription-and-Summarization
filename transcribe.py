# transcribe.py

import logging
import whisper

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def audio_to_text_whisper(audio_file):
    try:
        logging.info("Loading Whisper model...")
        model = whisper.load_model("base")  # Pilihan: "tiny", "base", "small", "medium", "large"
        logging.info(f"Transcribing audio file: {audio_file}")
        result = model.transcribe(audio_file, language="id")
        return result["text"]
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return f"Error during transcription: {e}"
