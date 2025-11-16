# Vibe - Chord Progression Generator

An intelligent music tool that helps you generate chord progression suggestions for your melodies. Built with React, TypeScript, Tone.js, and FastAPI.

## Features

- Interactive piano keyboard (2 octaves)
- Real-time melody input with audio feedback
- **Dual key detection algorithms**:
  - **HMM (Hidden Markov Model)**: Probabilistic model using Viterbi algorithm for detecting key modulations
  - **Scoring**: Fast frequency-based algorithm with sliding window analysis
- **Chromatic color visualization**: Each key is assigned a unique color from the chromatic circle
- **Sliding window tonality detection**: Shows local key changes throughout the melody
- 2 harmonic chord suggestions per note based on music theory scoring
- Playable chord preview with audio feedback
- Beautiful gradient UI with color-coded tonalities

## Architecture

- **Frontend**: React + TypeScript + Vite + Tone.js + Tailwind CSS
- **Backend**: Python + FastAPI + NumPy
- **Music Theory**:
  - Custom harmony engine with intelligent chord scoring
  - Hidden Markov Model for probabilistic key detection
  - Chromatic color palette based on HSL color space

## Setup

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Usage

1. Start both backend and frontend servers
2. Open your browser to `http://localhost:5173`
3. Select your preferred key detection algorithm (HMM or Scoring)
4. Click on the piano keys to build your melody
5. Click "Get Chord Suggestions" (or "Regenerate") to analyze your melody
6. View the detected key with color-coded visualization
7. Select chord suggestions for each note (checkboxes)
8. Click on melody notes to hear them with the selected chord
9. Use "Clear" to start over with a new melody

## Music Theory

### Key Detection Algorithms

**HMM (Hidden Markov Model)**:
- 24 hidden states (12 major + 12 minor keys)
- 12 observed states (chromatic notes)
- Transition matrix based on circle of fifths (close keys = higher probability)
- Emission matrix based on scale degree importance (tonic/dominant = high, chromatic = low)
- Viterbi algorithm finds optimal key sequence across entire melody
- Best for detecting modulations and key changes

**Scoring Algorithm**:
- Sliding window analysis (default: 6 notes)
- Frequency-based scoring weighted by note importance
- Faster computation for simple melodies
- Per-note tonality detection with local context

### Chord Suggestions

The harmony engine uses:
- Diatonic chord generation (I, ii, iii, IV, V, vi, vii°)
- Intelligent scoring system based on:
  - Melodic note position in chord (root/third/fifth)
  - Chord function strength (tonic/dominant/subdominant)
  - Harmonic context (previous and next chords)
- 2 best-scored chords per melody note
- Simple triads (major, minor, diminished) with quality explanations

## Development

### Backend Structure
```
backend/
├── main.py             # FastAPI application and endpoints
├── harmony_engine.py   # Harmony engine with HMM and chord scoring
├── music_theory.py     # Music theory fundamentals (scales, chords)
├── music_palette.py    # Chromatic color generation for tonalities
├── test_hmm.py         # HMM validation tests
└── requirements.txt    # Python dependencies (FastAPI, NumPy, etc.)
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── Piano.tsx              # Interactive piano keyboard
│   │   └── MelodyWithChords.tsx   # Melody visualization with chord suggestions
│   ├── utils/
│   │   └── noteConverter.ts       # French/English note conversion
│   ├── App.tsx                    # Main application with algorithm selector
│   └── index.css                  # Tailwind styles
└── package.json
```

### VS Code Debugging

A debug configuration is available in `.vscode/launch.json` for the backend:
```bash
# Make sure you're using the correct Python interpreter
# Set breakpoints in VS Code and press F5 to start debugging
```

## Future Enhancements

- Support for seventh chords and extended harmonies
- Chord inversions
- MIDI file import/export
- Save and load progressions
- Rhythm and timing information
- Multiple instrument sounds
- Audio recording and export
- Real-time analysis while playing

## License

MIT
