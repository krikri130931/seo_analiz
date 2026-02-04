# Video Transcription with ChatGPT (OpenAI)

This repo provides a small CLI script that extracts audio from a video file and sends it to the OpenAI API for transcription.

## Prerequisites

- Python 3.9+
- `ffmpeg` installed and available in your PATH
- An OpenAI API key

## Step-by-step setup (quick start)

1) Install `ffmpeg` and Python 3.9+.
   - macOS (Homebrew): `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y ffmpeg`
   - Windows (winget): `winget install ffmpeg`

2) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3) Install Python dependencies:

```bash
pip install -r requirements.txt
```

4) Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your_key_here"
```

5) Run the transcription:

```bash
python transcribe_video.py /path/to/video.mp4
```

## Usage

```bash
python transcribe_video.py /path/to/video.mp4
```

Optional arguments:

- `--model` (default: `gpt-4o-mini-transcribe`)
- `--language` (e.g. `ru`, `en`)
- `--output` (path to save transcript; prints to stdout if not provided)

Example:

```bash
python transcribe_video.py video.mp4 --language ru --output transcript.txt
```

## Notes

- The script creates a temporary WAV file during processing and removes it after transcription.
- The transcription uses the OpenAI Audio API.
