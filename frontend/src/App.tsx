import { useState } from 'react';
import Piano from './components/Piano';
import MelodyWithChords from './components/MelodyWithChords';

interface ChordOption {
  name: string;
  notes: string[];
  quality: string;
}

interface ChordSuggestion {
  note: string;
  chord_options: ChordOption[];
}

function App() {
  const [melody, setMelody] = useState<string[]>([]);
  const [suggestions, setSuggestions] = useState<ChordSuggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleNotePlay = (note: string) => {
    setMelody((prev) => [...prev, note]);
  };

  const handleClear = () => {
    setMelody([]);
    setSuggestions([]);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (melody.length === 0) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/suggest-chords', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ notes: melody }),
      });

      if (!response.ok) {
        throw new Error('Failed to get chord suggestions');
      }

      const data = await response.json();
      setSuggestions(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error fetching chord suggestions:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-2 drop-shadow-lg">
            Vibe
          </h1>
          <p className="text-xl text-white/90">
            Générateur de progressions d'accords
          </p>
          <p className="text-sm text-white/70 mt-2">
            Jouez une mélodie et obtenez des suggestions d'accords harmoniques
          </p>
        </div>

        {/* Piano */}
        <div className="mb-6">
          <Piano onNotePlay={handleNotePlay} />
        </div>

        {/* Melody with Chords */}
        <div className="mb-6">
          <MelodyWithChords
            melody={melody}
            suggestions={suggestions}
            onClear={handleClear}
            onAnalyze={handleAnalyze}
            isLoading={isLoading}
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border-2 border-red-400 rounded-lg">
            <p className="text-red-800 font-semibold">Erreur: {error}</p>
            <p className="text-red-600 text-sm mt-1">
              Assurez-vous que le serveur backend tourne sur http://localhost:8000
            </p>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-8 text-white/60 text-sm">
          <p>
            Développé avec React, TypeScript, Tone.js et FastAPI
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
