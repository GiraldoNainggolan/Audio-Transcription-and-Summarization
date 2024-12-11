# suara_mp3.py

# from flask import Flask, render_template, request, redirect, url_for
import os
import logging
from pydub import AudioSegment
from pydub.playback import play
from transcribe import audio_to_text_whisper
from summarize import summarize_text


# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Set path FFmpeg untuk pydub
ffmpeg_path = r"D:/py/ffmpeg/bin"
AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")
os.environ["PATH"] += os.pathsep + ffmpeg_path

def process_audio(input_audio):
    logging.info(f"Processing audio file: {input_audio}")

    # Periksa apakah file input ada
    if not os.path.exists(input_audio):
        logging.error(f"Audio file not found: {input_audio}")
    else:
        # Transkripsi MP3 ke teks menggunakan Whisper
        transcribed_text = audio_to_text_whisper(input_audio)

        if "Error" not in transcribed_text:
            logging.info("Transcription successful.")
            print("Transcribed Text:\n", transcribed_text)

            # Ringkasan teks
            summarized_text = summarize_text(transcribed_text)
            if "Error" not in summarized_text:
                print("\nSummarized Text:\n", summarized_text)
            else:
                logging.error(summarized_text)
        else:
            logging.error(transcribed_text)

        # Informasi tentang file audio
        try:
            audio = AudioSegment.from_file(input_audio)
            logging.info(f"Audio duration: {len(audio) / 1000} seconds")
            logging.info(f"Sample rate: {audio.frame_rate} Hz")
            logging.info(f"Channels: {audio.channels}")

            # (Opsional) Putar audio untuk memverifikasi
            logging.info("Playing audio...")
            play(audio)
        except Exception as e:
            logging.error(f"Error processing audio file: {e}")

if __name__ == "__main__":
    input_audio = "D:/py/suara.mp3"  # Ganti dengan path file audio yang sesuai
    process_audio(input_audio)
