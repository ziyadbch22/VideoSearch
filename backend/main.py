```python
import json
import os

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from transcribe import transcribe_video


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# CHEMINS
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

TRANSCRIPTION_FILE = os.path.join(
    BASE_DIR,
    "transcription.json"
)

VIDEOS_DIR = os.path.join(
    BASE_DIR,
    "videos"
)


CURRENT_VIDEO = os.path.join(
    VIDEOS_DIR,
    "test.mp4"
)


# =========================
# CHARGEMENT TRANSCRIPTION
# =========================

if os.path.exists(TRANSCRIPTION_FILE):

    with open(
        TRANSCRIPTION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        transcription = json.load(file)

else:

    transcription = {
        "language": "",
        "segments": []
    }


# =========================
# ROUTE PRINCIPALE
# =========================

@app.get("/")
def root():

    return {
        "message": "VideoSearch API fonctionne !"
    }


# =========================
# RECHERCHE
# =========================

@app.get("/search")
def search(q: str):

    results = []

    for segment in transcription["segments"]:

        if q.lower() in segment["text"].lower():

            results.append(segment)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }


# =========================
# VIDÉO ACTUELLE
# =========================

@app.get("/video")
def get_video():

    return FileResponse(
        CURRENT_VIDEO,
        media_type="video/mp4"
    )


# =========================
# UPLOAD + TRANSCRIPTION
# =========================

@app.post("/upload")
async def upload_video(
    file: UploadFile = File(...)
):

    global transcription
    global CURRENT_VIDEO

    os.makedirs(
        VIDEOS_DIR,
        exist_ok=True
    )


    # -------------------------
    # Sauvegarde de la vidéo
    # -------------------------

    file_path = os.path.join(
        VIDEOS_DIR,
        file.filename
    )


    with open(
        file_path,
        "wb"
    ) as buffer:

        while True:

            chunk = await file.read(
                1024 * 1024
            )

            if not chunk:
                break

            buffer.write(chunk)


    print(
        f"Vidéo reçue : {file.filename}"
    )


    # -------------------------
    # Vidéo actuelle
    # -------------------------

    CURRENT_VIDEO = file_path


    # -------------------------
    # Transcription Whisper
    # -------------------------

    print(
        "Début de la transcription..."
    )


    transcription = transcribe_video(
        file_path
    )


    # -------------------------
    # Sauvegarde JSON
    # -------------------------

    with open(
        TRANSCRIPTION_FILE,
        "w",
        encoding="utf-8"
    ) as json_file:

        json.dump(
            transcription,
            json_file,
            ensure_ascii=False,
            indent=2
        )


    print(
        "Transcription terminée !"
    )

    print(
        f"Langue : {transcription['language']}"
    )

    print(
        f"Segments : {len(transcription['segments'])}"
    )


    return {

        "message":
            "Vidéo uploadée et transcrite avec succès",

        "filename":
            file.filename,

        "language":
            transcription["language"],

        "segments":
            len(transcription["segments"])
    }
```
