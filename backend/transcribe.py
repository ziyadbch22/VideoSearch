import json
import os

from faster_whisper import WhisperModel


# Chargement du modèle Whisper
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def transcribe_video(video_path):
    """
    Transcrit une vidéo et retourne la transcription.
    """

    print(f"Transcription de : {video_path}")

    segments, info = model.transcribe(
        video_path,
        beam_size=5
    )

    transcription = {
        "language": info.language,
        "segments": []
    }

    for segment in segments:
        transcription["segments"].append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        })

    return transcription