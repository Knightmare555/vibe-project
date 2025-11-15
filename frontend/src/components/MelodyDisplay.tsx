import { convertNoteToFrench } from '../utils/noteConverter';

interface MelodyDisplayProps {
  notes: string[];
  onClear: () => void;
  onAnalyze: () => void;
  isLoading: boolean;
}

const MelodyDisplay = ({ notes, onClear, onAnalyze, isLoading }: MelodyDisplayProps) => {
  return (
    <div className="bg-white rounded-lg shadow-2xl p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-gray-800">Your Melody</h3>
        <div className="flex gap-2">
          <button
            onClick={onClear}
            disabled={notes.length === 0}
            className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600
                       disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            Clear
          </button>
          <button
            onClick={onAnalyze}
            disabled={notes.length === 0 || isLoading}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700
                       disabled:bg-indigo-300 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Analyzing...' : 'Get Chord Suggestions'}
          </button>
        </div>
      </div>

      <div className="min-h-20">
        {notes.length === 0 ? (
          <p className="text-gray-400 text-center py-8">
            Start playing notes on the piano above
          </p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {notes.map((note, index) => (
              <div
                key={index}
                className="px-4 py-2 bg-indigo-100 text-indigo-800 rounded-lg
                           font-semibold shadow-sm"
              >
                {convertNoteToFrench(note)}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MelodyDisplay;
