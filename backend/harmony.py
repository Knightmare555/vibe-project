"""
Harmony Engine - Generates chord suggestions based on music theory
"""
from collections import Counter


class HarmonyEngine:
    # Chromatic scale
    NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    # Major scale intervals (in semitones from root)
    MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]

    # Chord qualities for each degree in major scale
    # I, ii, iii, IV, V, vi, vii°
    DEGREE_QUALITIES = ["major", "minor", "minor", "major", "major", "minor", "diminished"]

    def __init__(self):
        pass

    def strip_octave(self, note: str) -> str:
        """Remove octave number from note (e.g., 'C4' -> 'C')"""
        return ''.join([c for c in note if not c.isdigit()])

    def get_note_index(self, note: str) -> int:
        """Get chromatic index of a note"""
        return self.NOTES.index(note)

    def transpose_note(self, note: str, semitones: int) -> str:
        """Transpose a note by semitones"""
        idx = self.get_note_index(note)
        new_idx = (idx + semitones) % 12
        return self.NOTES[new_idx]

    def build_major_scale(self, root: str) -> list[str]:
        """Build a major scale from a root note"""
        scale = []
        for interval in self.MAJOR_SCALE:
            scale.append(self.transpose_note(root, interval))
        return scale

    def build_chord(self, root: str, quality: str) -> list[str]:
        """Build a triad chord"""
        root_idx = self.get_note_index(root)

        if quality == "major":
            intervals = [0, 4, 7]  # Root, Major 3rd, Perfect 5th
        elif quality == "minor":
            intervals = [0, 3, 7]  # Root, Minor 3rd, Perfect 5th
        elif quality == "diminished":
            intervals = [0, 3, 6]  # Root, Minor 3rd, Diminished 5th
        else:
            intervals = [0, 4, 7]

        chord_notes = []
        for interval in intervals:
            note_idx = (root_idx + interval) % 12
            chord_notes.append(self.NOTES[note_idx])

        return chord_notes

    def detect_key(self, melody_notes: list[str]) -> str:
        """
        Simple key detection: find which major key contains most of these notes
        """
        # Strip octaves
        unique_notes = set(self.strip_octave(note) for note in melody_notes)

        # Try all possible keys
        best_key = "C"
        best_match = 0

        for potential_key in self.NOTES:
            scale = self.build_major_scale(potential_key)
            matches = sum(1 for note in unique_notes if note in scale)
            if matches > best_match:
                best_match = matches
                best_key = potential_key

        return best_key

    def get_chords_containing_note(self, note: str, key: str) -> list[dict[str, any]]:
        """
        Get all diatonic chords in the key that contain the given note
        """
        scale = self.build_major_scale(key)
        chords = []

        for degree_idx, scale_note in enumerate(scale):
            quality = self.DEGREE_QUALITIES[degree_idx]
            chord_notes = self.build_chord(scale_note, quality)

            if note in chord_notes:
                chord_name = self.format_chord_name(scale_note, quality)
                chords.append({
                    "root": scale_note,
                    "quality": quality,
                    "name": chord_name,
                    "notes": chord_notes,
                    "degree": degree_idx + 1
                })

        return chords

    def format_chord_name(self, root: str, quality: str) -> str:
        """Format chord name (e.g., 'C major' -> 'C', 'D minor' -> 'Dm')"""
        if quality == "major":
            return root
        elif quality == "minor":
            return f"{root}m"
        elif quality == "diminished":
            return f"{root}°"
        return root

    def select_best_chord_progression(self, available_chords: list[list[dict]],
                                       melody_notes: list[str]) -> list[list[dict]]:
        """
        Select the best 2 chord options for each note
        Prioritize: I, V, IV, vi, ii, iii, vii°
        """
        DEGREE_PRIORITY = [1, 5, 4, 6, 2, 3, 7]

        result = []
        for note_chords in available_chords:
            # Sort by degree priority
            sorted_chords = sorted(
                note_chords,
                key=lambda c: DEGREE_PRIORITY.index(c["degree"]) if c["degree"] in DEGREE_PRIORITY else 10
            )
            # Take top 2
            result.append(sorted_chords[:2])

        return result

    def generate_chord_suggestions(self, melody_notes: list[str]) -> list[dict]:
        """
        Main function: generate 2 chord suggestions for each note in the melody
        """
        if not melody_notes:
            return []

        # Detect key
        detected_key = self.detect_key(melody_notes)

        # For each note, find possible chords
        all_suggestions = []
        for note_with_octave in melody_notes:
            note = self.strip_octave(note_with_octave)
            possible_chords = self.get_chords_containing_note(note, detected_key)
            all_suggestions.append(possible_chords)

        # Select best 2 for each note
        best_suggestions = self.select_best_chord_progression(all_suggestions, melody_notes)

        # Format response
        response = []
        for idx, note in enumerate(melody_notes):
            chord_options = [
                {
                    "name": chord["name"],
                    "notes": chord["notes"],
                    "quality": chord["quality"]
                }
                for chord in best_suggestions[idx]
            ]

            response.append({
                "note": note,
                "chord_options": chord_options
            })

        return response
