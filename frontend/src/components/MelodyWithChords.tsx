import { useState, useRef, useEffect } from 'react';
import * as Tone from 'tone';
import { convertNoteToFrench, convertChordNameToFrench } from '../utils/noteConverter';

interface ChordOption {
  name: string;
  notes: string[];
  quality: string;
}

interface ChordSuggestion {
  note: string;
  chord_options: ChordOption[];
}

interface MelodyWithChordsProps {
  melody: string[];
  suggestions: ChordSuggestion[];
  onClear: () => void;
  onAnalyze: () => void;
  isLoading: boolean;
}

interface SelectedChord {
  noteIndex: number;
  chordIndex: number;
}

const MelodyWithChords = ({
  melody,
  suggestions,
  onClear,
  onAnalyze,
  isLoading
}: MelodyWithChordsProps) => {
  const [selectedChords, setSelectedChords] = useState<SelectedChord[]>([]);
  const synthRef = useRef<Tone.PolySynth | null>(null);

  useEffect(() => {
    // Initialize Tone.js synth
    synthRef.current = new Tone.PolySynth(Tone.Synth).toDestination();
    synthRef.current.set({
      envelope: {
        attack: 0.02,
        decay: 0.2,
        sustain: 0.5,
        release: 1.5,
      },
    });

    return () => {
      synthRef.current?.dispose();
    };
  }, []);

  // Réinitialiser les sélections quand la mélodie change (longueur différente)
  useEffect(() => {
    setSelectedChords((prev) => {
      // Garder seulement les sélections dont l'index existe encore dans la nouvelle mélodie
      return prev.filter((sc) => sc.noteIndex < melody.length);
    });
  }, [melody.length]);

  const toggleChord = (noteIndex: number, chordIndex: number) => {
    setSelectedChords((prev) => {
      const existing = prev.find(
        (sc) => sc.noteIndex === noteIndex && sc.chordIndex === chordIndex
      );

      if (existing) {
        // Désélectionner
        return prev.filter(
          (sc) => !(sc.noteIndex === noteIndex && sc.chordIndex === chordIndex)
        );
      } else {
        // Sélectionner (et désélectionner l'autre accord pour cette note si présent)
        const filtered = prev.filter((sc) => sc.noteIndex !== noteIndex);
        return [...filtered, { noteIndex, chordIndex }];
      }
    });
  };

  const isChordSelected = (noteIndex: number, chordIndex: number): boolean => {
    return selectedChords.some(
      (sc) => sc.noteIndex === noteIndex && sc.chordIndex === chordIndex
    );
  };

  const playNoteWithChords = async (noteIndex: number) => {
    if (Tone.context.state !== 'running') {
      await Tone.start();
    }

    if (!synthRef.current) return;

    // Jouer la note
    const note = melody[noteIndex];
    synthRef.current.triggerAttackRelease(note, '8n');

    // Trouver et jouer l'accord sélectionné pour cette note
    const selectedChord = selectedChords.find((sc) => sc.noteIndex === noteIndex);
    if (selectedChord && suggestions[noteIndex]) {
      const chord = suggestions[noteIndex].chord_options[selectedChord.chordIndex];
      if (chord) {
        // Jouer l'accord légèrement après la note
        setTimeout(() => {
          const fullNotes = chord.notes.map((n) =>
            n.includes('4') || n.includes('5') ? n : `${n}4`
          );
          synthRef.current?.triggerAttackRelease(fullNotes, '2n');
        }, 100);
      }
    }
  };

  if (melody.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-2xl p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold text-gray-800">Votre mélodie</h3>
        </div>
        <p className="text-gray-400 text-center py-8">
          Commencez à jouer des notes sur le piano
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-2xl p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-bold text-gray-800">Votre mélodie</h3>
        <div className="flex gap-2">
          <button
            onClick={onClear}
            className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600
                       transition-colors"
          >
            Effacer
          </button>
          <button
            onClick={onAnalyze}
            disabled={isLoading}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700
                       disabled:bg-indigo-300 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Analyse...' : suggestions.length > 0 ? 'Régénérer' : 'Obtenir les suggestions'}
          </button>
        </div>
      </div>

      {/* Melody with chords grid */}
      <div className="overflow-x-auto">
        <div className="inline-flex gap-2 min-w-full">
          {melody.map((note, noteIndex) => {
            const suggestion = suggestions[noteIndex];

            return (
              <div key={noteIndex} className="flex flex-col items-center gap-2 min-w-[140px]">
                {/* Note de la mélodie */}
                <button
                  onClick={() => playNoteWithChords(noteIndex)}
                  className="w-full px-4 py-3 bg-indigo-600 text-white rounded-lg
                             font-bold text-lg hover:bg-indigo-700 active:bg-indigo-800
                             transition-colors shadow-md cursor-pointer"
                >
                  {convertNoteToFrench(note)}
                </button>

                {/* Suggestions d'accords */}
                {suggestion && suggestion.chord_options.length > 0 ? (
                  <div className="w-full flex flex-col gap-2">
                    {suggestion.chord_options.map((chord, chordIndex) => {
                      const selected = isChordSelected(noteIndex, chordIndex);
                      const qualityFr =
                        chord.quality === 'major'
                          ? 'majeur'
                          : chord.quality === 'minor'
                          ? 'mineur'
                          : chord.quality === 'diminished'
                          ? 'diminué'
                          : chord.quality;

                      return (
                        <label
                          key={chordIndex}
                          className={`flex items-start gap-2 p-3 rounded-lg border-2 cursor-pointer
                                     transition-all ${
                                       selected
                                         ? 'bg-purple-50 border-purple-400'
                                         : 'bg-gray-50 border-gray-200 hover:border-purple-300'
                                     }`}
                        >
                          <input
                            type="checkbox"
                            checked={selected}
                            onChange={() => toggleChord(noteIndex, chordIndex)}
                            className="mt-1 h-4 w-4 text-purple-600 rounded focus:ring-purple-500"
                          />
                          <div className="flex-1 text-left">
                            <div className="font-semibold text-gray-800">
                              {convertChordNameToFrench(chord.name)}
                            </div>
                            <div className="text-xs text-gray-500">
                              {chord.notes.map(convertNoteToFrench).join(' · ')}
                            </div>
                            <div className="text-xs text-gray-400 italic mt-1">
                              {qualityFr}
                            </div>
                          </div>
                        </label>
                      );
                    })}
                  </div>
                ) : (
                  <div className="w-full h-32 flex items-center justify-center text-gray-400 text-sm border-2 border-dashed border-gray-200 rounded-lg">
                    {isLoading ? 'Analyse...' : 'Pas de suggestions'}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Info message */}
      {suggestions.length > 0 && (
        <div className="mt-6 p-4 bg-indigo-50 rounded-lg">
          <p className="text-sm text-indigo-800">
            <strong>Astuce :</strong> Sélectionnez un accord pour chaque note, puis cliquez
            sur la note pour entendre la note avec l'accord !
          </p>
        </div>
      )}
    </div>
  );
};

export default MelodyWithChords;
