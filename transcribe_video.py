import argparse
import os
import subprocess
import tempfile
from pathlib import Path

from openai import OpenAI


def extract_audio(video_path: Path, sample_rate: int = 16000) -> Path:
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_file.close()
    output_path = Path(temp_file.name)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        str(output_path),
    ]
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path


def transcribe_audio(audio_path: Path, model: str, language: str | None) -> str:
    client = OpenAI()
    with audio_path.open("rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            language=language,
        )
    return response.text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transcribe a video using OpenAI.")
    parser.add_argument("video", type=Path, help="Path to the video file")
    parser.add_argument(
        "--model",
        default="gpt-4o-mini-transcribe",
        help="OpenAI transcription model",
    )
    parser.add_argument("--language", default=None, help="Language hint (e.g. ru, en)")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output file for the transcript",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.video.exists():
        raise FileNotFoundError(f"Video not found: {args.video}")
    if "OPENAI_API_KEY" not in os.environ:
        raise EnvironmentError("OPENAI_API_KEY is not set")

    audio_path = extract_audio(args.video)
    try:
        transcript = transcribe_audio(audio_path, args.model, args.language)
    finally:
        audio_path.unlink(missing_ok=True)

    if args.output:
        args.output.write_text(transcript, encoding="utf-8")
    else:
        print(transcript)


if __name__ == "__main__":
    main()
