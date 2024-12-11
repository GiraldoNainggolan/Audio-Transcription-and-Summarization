# summarize.py

import logging
from transformers import pipeline

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def summarize_text(text):
    try:
        logging.info("Summarizing text...")
        summarizer = pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")
        summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error during summarization: {e}")
        return f"Error summarizing text: {e}"
