import { useEffect, useRef } from 'react';
import * as Tone from 'tone';
import { convertNoteToFrench } from '../utils/noteConverter';

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
    { note: 'C4', label: 'Do' },
    { note: 'D4', label: 'Ré' },
    { note: 'E4', label: 'Mi' },
    { note: 'F4', label: 'Fa' },
    { note: 'G4', label: 'Sol' },
    { note: 'A4', label: 'La' },
    { note: 'B4', label: 'Si' },
    { note: 'C5', label: 'Do' },
    { note: 'D5', label: 'Ré' },
    { note: 'E5', label: 'Mi' },
    { note: 'F5', label: 'Fa' },
    { note: 'G5', label: 'Sol' },
    { note: 'A5', label: 'La' },
    { note: 'B5', label: 'Si' },
  ];

  // Calcul des positions des touches noires (à la frontière entre les touches blanches)
  // 14 touches blanches, chaque touche = 100/14 = 7.14%
  const keyWidth = 100 / 14; // 7.14%
  const blackKeys = [
    { note: 'C#4', left: `${keyWidth * 1}%` },        // Entre C4 (0) et D4 (1)
    { note: 'D#4', left: `${keyWidth * 2}%` },        // Entre D4 (1) et E4 (2)
    { note: 'F#4', left: `${keyWidth * 4}%` },        // Entre F4 (3) et G4 (4)
    { note: 'G#4', left: `${keyWidth * 5}%` },        // Entre G4 (4) et A4 (5)
    { note: 'A#4', left: `${keyWidth * 6}%` },        // Entre A4 (5) et B4 (6)
    { note: 'C#5', left: `${keyWidth * 8}%` },        // Entre C5 (7) et D5 (8)
    { note: 'D#5', left: `${keyWidth * 9}%` },        // Entre D5 (8) et E5 (9)
    { note: 'F#5', left: `${keyWidth * 11}%` },       // Entre F5 (10) et G5 (11)
    { note: 'G#5', left: `${keyWidth * 12}%` },       // Entre G5 (11) et A5 (12)
    { note: 'A#5', left: `${keyWidth * 13}%` },       // Entre A5 (12) et B5 (13)
  ];

  return (
    <div className="bg-white rounded-lg shadow-2xl p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">
        Piano
      </h2>
      <p className="text-sm text-gray-600 mb-6 text-center">
        Cliquez sur les touches pour composer votre mélodie
      </p>

      <div className="relative h-48">
        {/* White keys */}
        <div className="flex w-full h-full">
          {whiteKeys.map((key) => (
            <button
              key={key.note}
              onClick={() => playNote(key.note)}
              className="flex-1 h-full bg-white border-2 border-gray-300 rounded-b-lg
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
            style={{
              left: key.left,
              transform: 'translateX(-50%)'
            }}
            className="absolute top-0 h-28 w-9 bg-gray-900 rounded-b-lg
                       hover:bg-gray-700 active:bg-gray-600 transition-colors
                       shadow-lg z-10"
          />
        ))}
      </div>
    </div>
  );
};

export default Piano;
