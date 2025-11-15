from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from harmony import HarmonyEngine

app = FastAPI(title="Vibe - Chord Progression Generator")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

harmony_engine = HarmonyEngine()


class MelodyRequest(BaseModel):
    notes: List[str]  # e.g., ["C4", "E4", "G4", "A4"]


class ChordOption(BaseModel):
    name: str
    notes: List[str]
    quality: str


class ChordSuggestion(BaseModel):
    note: str
    chord_options: List[ChordOption]


@app.get("/")
async def root():
    return {"message": "Vibe API is running"}


@app.post("/suggest-chords", response_model=List[ChordSuggestion])
async def suggest_chords(request: MelodyRequest):
    """
    Given a melody (list of notes), suggest 2 chord options for each note.
    """
    suggestions = harmony_engine.generate_chord_suggestions(request.notes)
    return suggestions


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
