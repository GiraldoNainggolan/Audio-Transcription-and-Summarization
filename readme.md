# Audio Transcription and Summarization Project

This project transcribes audio files into text using the Whisper model and summarizes the transcribed text using the mT5 model. It uses PyDub for audio handling and Hugging Face's transformers library for summarization.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Requirements](#requirements)
3. [Installation Instructions](#installation-instructions)
4. [Usage Instructions](#usage-instructions)
5. [File Structure](#file-structure)
6. [License](#license)
7. [Acknowledgments](#acknowledgments)

## Project Overview

This project involves:
1. **Audio File Processing**: Audio files (e.g., MP3 format) are read and processed using the PyDub library.
2. **Transcription**: The audio file is transcribed into text using OpenAI's Whisper model.
3. **Summarization**: The transcribed text is then summarized using the `mT5` multilingual model from Hugging Face's transformers library.

The goal is to provide an easy way to transcribe and summarize audio files in multiple languages, including Indonesian.

## Requirements

Before running the project, you need the following:
- **Python 3.8 or higher**
- **FFmpeg**: Required for audio processing (make sure it is installed and added to your system's PATH).
- **PyDub**: For audio file handling.
- **Whisper**: For transcription (OpenAI's model).
- **Transformers**: Hugging Face's transformers library for text summarization.
- **Torch**: PyTorch, necessary for running Whisper and transformers models.

### Install the required Python libraries:
```bash
pip install pydub whisper transformers torch
```


# FFmpeg Installation:
You need to install FFmpeg on your system for PyDub to process audio files. You can download it from the [FFmpeg official website](https://ffmpeg.org/download.html).

Once downloaded, make sure FFmpeg is accessible via your system's PATH, or specify the path directly in the script.

# Installation Instructions
## Step 1: Clone the Repository
Clone this repository to your local machine:

```bash
https://github.com/GiraldoNainggolan/Audio-Transcription-and-Summarization.git
cd yourrepository
```

## Step 2: Set Up a Virtual Environment
Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

## Step 3: Install Dependencies
Install the required dependencies:

```bash
Salin kode
pip install -r requirements.txt
```

## Step 4: Set Up FFmpeg
Download FFmpeg from the official site and add it to your system's PATH. On Windows, this can be done by modifying the Environment Variables.

Alternatively, specify the path to FFmpeg directly in the suara_mp3.py file by setting the ffmpeg_path variable.

# Usage Instructions
## Step 1: Prepare the Audio File
Place the audio file (e.g., suara.mp3) in the project directory.

## Step 2: Run the suara_mp3.py Script
Execute the script to transcribe and summarize the audio file:

```bash
python suara_mp3.py
```

The script will:

1. Transcribe the audio file into text using Whisper.
2. Summarize the transcribed text using the mT5 multilingual model.
3. Display information about the audio file (duration, sample rate, and channels).
4. Optionally, play back the audio for verification.


# File Structure
Here’s a summary of the project’s directory structure:

```bash
Salin kode
my_project/
├── .venv/                      # Virtual environment
├── ffmpeg/                     # FFmpeg binaries
│   ├── ffmpeg.exe              # FFmpeg executable
│   ├── ffplay.exe              # FFPlay executable
│   └── ffprobe.exe             # FFProbe executable
├── suara.mp3                   # Input audio file
├── suara_mp3.py                # Main script for processing
├── transcribe.py               # Audio transcription script
├── summarize.py                # Text summarization script
├── requirements.txt            # Python dependencies file
└── README.md                   # Project documentation
```

# License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- OpenAI Whisper for the transcription model.
- Hugging Face Transformers for the summarization model.
- PyDub for audio processing.
- FFmpeg for audio file format conversion.

```bash
Salinlah kode di atas ke dalam file **`README.md`**, dan Anda siap menggunakan file dokumentasi proyek ini!
```
