import { useRef, useEffect } from 'react';
import * as Tone from 'tone';

interface ChordOption {
  name: string;
  notes: string[];
  quality: string;
}

interface ChordSuggestion {
  note: string;
  chord_options: ChordOption[];
}

interface ChordSuggestionsProps {
  suggestions: ChordSuggestion[];
}

const ChordSuggestions = ({ suggestions }: ChordSuggestionsProps) => {
  const synthRef = useRef<Tone.PolySynth | null>(null);

  useEffect(() => {
    // Initialize Tone.js synth for playing chords
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

  const playChord = async (notes: string[]) => {
    if (Tone.context.state !== 'running') {
      await Tone.start();
    }

    if (synthRef.current) {
      // Add octave to notes if not present and play as chord
      const fullNotes = notes.map(note => note.includes('4') || note.includes('5') ? note : `${note}4`);
      synthRef.current.triggerAttackRelease(fullNotes, '2n');
    }
  };

  if (suggestions.length === 0) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-2xl p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Chord Suggestions</h3>

      <div className="space-y-4">
        {suggestions.map((suggestion, index) => (
          <div key={index} className="border-l-4 border-indigo-500 pl-4">
            <div className="text-sm font-semibold text-gray-600 mb-2">
              For note: <span className="text-indigo-700 text-lg">{suggestion.note}</span>
            </div>

            <div className="flex flex-wrap gap-3">
              {suggestion.chord_options.map((chord, chordIndex) => (
                <button
                  key={chordIndex}
                  onClick={() => playChord(chord.notes)}
                  className="group relative px-6 py-3 bg-gradient-to-r from-indigo-50 to-purple-50
                             border-2 border-indigo-200 rounded-lg hover:border-indigo-400
                             hover:shadow-lg transition-all duration-200"
                >
                  <div className="flex flex-col items-center">
                    <span className="text-lg font-bold text-indigo-700 group-hover:text-indigo-900">
                      {chord.name}
                    </span>
                    <span className="text-xs text-gray-500 mt-1">
                      {chord.notes.join(' - ')}
                    </span>
                    <span className="text-xs text-gray-400 italic mt-1">
                      {chord.quality}
                    </span>
                  </div>
                  <div className="absolute inset-0 bg-indigo-500 opacity-0 group-hover:opacity-10
                                  rounded-lg transition-opacity" />
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-indigo-50 rounded-lg">
        <p className="text-sm text-indigo-800">
          <strong>Tip:</strong> Click on any chord to hear how it sounds!
        </p>
      </div>
    </div>
  );
};

export default ChordSuggestions;
