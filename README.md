# Vibe - Chord Progression Generator

An intelligent music tool that helps you generate chord progression suggestions for your melodies. Built with React, TypeScript, Tone.js, and FastAPI.

## Features

- Interactive piano keyboard (2 octaves)
- Real-time melody input with audio feedback
- Automatic key detection
- 2 harmonic chord suggestions per note based on music theory
- Playable chord preview
- Beautiful gradient UI

## Architecture

- **Frontend**: React + TypeScript + Vite + Tone.js + Tailwind CSS
- **Backend**: Python + FastAPI
- **Music Theory**: Custom harmony engine with diatonic chord analysis

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
3. Click on the piano keys to build your melody
4. Click "Get Chord Suggestions" to analyze your melody
5. Click on suggested chords to hear how they sound
6. Use "Clear" to start over with a new melody

## Music Theory

The harmony engine uses:
- Automatic key detection based on note frequency analysis
- Diatonic chord generation (I, ii, iii, IV, V, vi, vii°)
- Smart chord prioritization (I, V, IV, vi most common)
- Simple triads (major, minor, diminished)

## Development

### Backend Structure
```
backend/
├── main.py          # FastAPI application and endpoints
├── harmony.py       # Harmony engine with music theory logic
└── requirements.txt # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── Piano.tsx            # Interactive piano keyboard
│   │   ├── MelodyDisplay.tsx    # Melody visualization
│   │   └── ChordSuggestions.tsx # Chord suggestions with audio
│   ├── App.tsx                  # Main application
│   └── index.css                # Tailwind styles
└── package.json
```

## Future Enhancements

- Support for seventh chords and extended harmonies
- Chord inversions
- MIDI file import/export
- Save and load progressions
- More sophisticated key detection (minor keys)
- Rhythm and timing information
- Multiple instrument sounds

## License

MIT
