import { useState } from 'react';
import Piano from './components/Piano';
import MelodyWithChords from './components/MelodyWithChords';

interface DetectedKey {
  tonalite: string;
  score: number;
}

interface ChordOption {
  name: string;
  notes: string[];
  quality: string;
  reason?: string;
}

interface ChordSuggestion {
  note: string;
  chord_options: ChordOption[];
  detected_key: string;
  key_candidates: DetectedKey[];
}

interface APIResponse {
  detected_keys: DetectedKey[];
  chosen_key: string;
  suggestions: ChordSuggestion[];
}

function App() {
  const [melody, setMelody] = useState<string[]>([]);
  const [suggestions, setSuggestions] = useState<ChordSuggestion[]>([]);
  const [detectedKeys, setDetectedKeys] = useState<DetectedKey[]>([]);
  const [chosenKey, setChosenKey] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [algorithm, setAlgorithm] = useState<'hmm' | 'scoring'>('hmm');

  const handleNotePlay = (note: string) => {
    setMelody((prev) => [...prev, note]);
  };

  const handleClear = () => {
    setMelody([]);
    setSuggestions([]);
    setDetectedKeys([]);
    setChosenKey('');
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
        body: JSON.stringify({
          notes: melody,
          algorithm: algorithm
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get chord suggestions');
      }

      const data: APIResponse = await response.json();
      setSuggestions(data.suggestions);
      setDetectedKeys(data.detected_keys);
      setChosenKey(data.chosen_key);
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

        {/* Algorithm Selector */}
        <div className="mb-6 bg-white/10 backdrop-blur-sm rounded-lg p-4">
          <div className="flex items-center justify-center gap-4">
            <span className="text-white font-medium">Algorithme de détection :</span>
            <div className="flex gap-2">
              <button
                onClick={() => setAlgorithm('hmm')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  algorithm === 'hmm'
                    ? 'bg-indigo-600 text-white shadow-lg'
                    : 'bg-white/20 text-white hover:bg-white/30'
                }`}
              >
                HMM (Markov)
              </button>
              <button
                onClick={() => setAlgorithm('scoring')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  algorithm === 'scoring'
                    ? 'bg-indigo-600 text-white shadow-lg'
                    : 'bg-white/20 text-white hover:bg-white/30'
                }`}
              >
                Scoring Simple
              </button>
            </div>
          </div>
          <div className="text-center mt-2 text-sm text-white/70">
            {algorithm === 'hmm'
              ? '🎯 Modèle de Markov Caché - Meilleur pour les modulations'
              : '⚡ Algorithme de scoring - Plus rapide et simple'}
          </div>
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
            detectedKeys={detectedKeys}
            chosenKey={chosenKey}
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
