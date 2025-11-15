import { useEffect, useRef } from 'react';
import * as Tone from 'tone';

interface PianoProps {
  onNotePlay: (note: string) => void;
}

const Piano = ({ onNotePlay }: PianoProps) => {
  const synthRef = useRef<Tone.PolySynth | null>(null);

  useEffect(() => {
    // Initialize Tone.js synth
    synthRef.current = new Tone.PolySynth(Tone.Synth).toDestination();
    synthRef.current.set({
      envelope: {
        attack: 0.02,
        decay: 0.1,
        sustain: 0.3,
        release: 1,
      },
    });

    return () => {
      synthRef.current?.dispose();
    };
  }, []);

  const playNote = async (note: string) => {
    // Start Tone.js audio context on first interaction
    if (Tone.context.state !== 'running') {
      await Tone.start();
    }

    if (synthRef.current) {
      synthRef.current.triggerAttackRelease(note, '8n');
      onNotePlay(note);
    }
  };

  // Piano keys: 2 octaves (C4 to B5)
  const whiteKeys = [
    { note: 'C4', label: 'C' },
    { note: 'D4', label: 'D' },
    { note: 'E4', label: 'E' },
    { note: 'F4', label: 'F' },
    { note: 'G4', label: 'G' },
    { note: 'A4', label: 'A' },
    { note: 'B4', label: 'B' },
    { note: 'C5', label: 'C' },
    { note: 'D5', label: 'D' },
    { note: 'E5', label: 'E' },
    { note: 'F5', label: 'F' },
    { note: 'G5', label: 'G' },
    { note: 'A5', label: 'A' },
    { note: 'B5', label: 'B' },
  ];

  const blackKeys = [
    { note: 'C#4', left: '7%' },
    { note: 'D#4', left: '14%' },
    { note: 'F#4', left: '28%' },
    { note: 'G#4', left: '35%' },
    { note: 'A#4', left: '42%' },
    { note: 'C#5', left: '57%' },
    { note: 'D#5', left: '64%' },
    { note: 'F#5', left: '78%' },
    { note: 'G#5', left: '85%' },
    { note: 'A#5', left: '92%' },
  ];

  return (
    <div className="bg-white rounded-lg shadow-2xl p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">
        Piano
      </h2>
      <p className="text-sm text-gray-600 mb-6 text-center">
        Click on the keys to build your melody
      </p>

      <div className="relative h-48 flex items-end">
        {/* White keys */}
        <div className="flex w-full">
          {whiteKeys.map((key) => (
            <button
              key={key.note}
              onClick={() => playNote(key.note)}
              className="flex-1 h-40 bg-white border-2 border-gray-300 rounded-b-lg
                         hover:bg-gray-100 active:bg-gray-200 transition-colors
                         flex items-end justify-center pb-4 text-sm font-medium text-gray-700
                         shadow-md"
            >
              {key.label}
            </button>
          ))}
        </div>

        {/* Black keys */}
        {blackKeys.map((key) => (
          <button
            key={key.note}
            onClick={() => playNote(key.note)}
            style={{ left: key.left }}
            className="absolute h-24 w-10 bg-gray-900 rounded-b-lg
                       hover:bg-gray-700 active:bg-gray-600 transition-colors
                       shadow-lg z-10"
          />
        ))}
      </div>
    </div>
  );
};

export default Piano;
