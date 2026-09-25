import json
import os

from faster_whisper import WhisperModel


# Chargement du modèle Whisper
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

# Transcription de la vidéo
segments, info = model.transcribe(
    "../videos/test.mp4",
    beam_size=5
)

# Préparation des résultats
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


# Sauvegarde dans un fichier JSON
output_path = os.path.abspath("../transcription.json")

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(transcription, file, ensure_ascii=False, indent=2)

print("Transcription terminée !")
print(f"Langue détectée : {info.language}")
print(f"Nombre de segments : {len(transcription['segments'])}")
print(f"Fichier créé ici : {output_path}")