from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from harmony_engine import HarmonyEngineV2

app = FastAPI(title="Vibe - Chord Progression Generator")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

harmony_engine = HarmonyEngineV2()


class MelodyRequest(BaseModel):
    notes: list[str]  # e.g., ["C4", "E4", "G4", "A4"]
    chosen_key: Optional[str] = None  # Tonalité choisie par l'utilisateur


class DetectedKey(BaseModel):
    tonalite: str
    score: float


class ChordOption(BaseModel):
    name: str
    notes: list[str]
    quality: str
    reason: Optional[str] = None  # Raison de la suggestion


class ChordSuggestion(BaseModel):
    note: str
    chord_options: list[ChordOption]


class SuggestionResponse(BaseModel):
    detected_keys: list[DetectedKey]
    chosen_key: str
    suggestions: list[ChordSuggestion]


@app.get("/")
async def root():
    return {"message": "Vibe API is running"}


@app.post("/suggest-chords", response_model=SuggestionResponse)
async def suggest_chords(request: MelodyRequest):
    """
    Analyse une mélodie et suggère des accords intelligemment.

    Retourne:
    - Les 3 tonalités les plus probables
    - La tonalité choisie (auto ou par l'utilisateur)
    - Les suggestions d'accords par note avec explications
    """
    result = harmony_engine.suggerer_accords_pour_melodie(
        melodie=request.notes,
        tonalite_choisie=request.chosen_key
    )
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
