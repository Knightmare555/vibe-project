/**
 * Convertit les notes de la notation anglaise vers la notation française (solfège)
 */

const NOTE_CONVERSION: Record<string, string> = {
  'C': 'Do',
  'C#': 'Do#',
  'Db': 'Réb',
  'D': 'Ré',
  'D#': 'Ré#',
  'Eb': 'Mib',
  'E': 'Mi',
  'F': 'Fa',
  'F#': 'Fa#',
  'Gb': 'Solb',
  'G': 'Sol',
  'G#': 'Sol#',
  'Ab': 'Lab',
  'A': 'La',
  'A#': 'La#',
  'Bb': 'Sib',
  'B': 'Si',
};

/**
 * Convertit une note avec octave (ex: "C4") en notation française
 */
export function convertNoteToFrench(note: string): string {
  // Extraire la note et l'octave
  const noteMatch = note.match(/^([A-G][#b]?)(\d*)$/);

  if (!noteMatch) {
    return note; // Retourner tel quel si format non reconnu
  }

  const [, noteName, octave] = noteMatch;
  const frenchNote = NOTE_CONVERSION[noteName];

  if (!frenchNote) {
    return note;
  }

  return octave ? `${frenchNote}${octave}` : frenchNote;
}

/**
 * Convertit un tableau de notes en notation française
 */
export function convertNotesToFrench(notes: string[]): string[] {
  return notes.map(convertNoteToFrench);
}

/**
 * Convertit un nom d'accord en notation française (ex: "Cm" -> "Dom")
 */
export function convertChordNameToFrench(chordName: string): string {
  // Extraire la note racine et le suffixe (m, °, etc.)
  const chordMatch = chordName.match(/^([A-G][#b]?)(.*)$/);

  if (!chordMatch) {
    return chordName;
  }

  const [, root, suffix] = chordMatch;
  const frenchRoot = NOTE_CONVERSION[root];

  if (!frenchRoot) {
    return chordName;
  }

  return `${frenchRoot}${suffix}`;
}
