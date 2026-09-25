import json
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("../transcription.json", "r", encoding="utf-8") as file:
    transcription = json.load(file)


@app.get("/")
def root():
    return {"message": "VideoSearch API fonctionne !"}


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
@app.get("/video")
def get_video():
    return FileResponse(
        "../videos/test.mp4",
        media_type="video/mp4"
    )