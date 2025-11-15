"""
Base de données musicales et structures de données pour la théorie musicale
"""

# 1. LES 24 GAMMES (12 majeures + 12 mineures naturelles)
GAMMES = {
    # Tonalités majeures
    "Do Majeur": ["C", "D", "E", "F", "G", "A", "B"],
    "Do# Majeur": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
    "Ré Majeur": ["D", "E", "F#", "G", "A", "B", "C#"],
    "Ré# Majeur": ["D#", "E#", "F##", "G#", "A#", "B#", "C##"],
    "Mi Majeur": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "Fa Majeur": ["F", "G", "A", "Bb", "C", "D", "E"],
    "Fa# Majeur": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "Sol Majeur": ["G", "A", "B", "C", "D", "E", "F#"],
    "Sol# Majeur": ["G#", "A#", "B#", "C#", "D#", "E#", "F##"],
    "La Majeur": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "La# Majeur": ["A#", "B#", "C##", "D#", "E#", "F##", "G##"],
    "Si Majeur": ["B", "C#", "D#", "E", "F#", "G#", "A#"],

    # Tonalités mineures naturelles
    "Do Mineur": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
    "Do# Mineur": ["C#", "D#", "E", "F#", "G#", "A", "B"],
    "Ré Mineur": ["D", "E", "F", "G", "A", "Bb", "C"],
    "Ré# Mineur": ["D#", "E#", "F#", "G#", "A#", "B", "C#"],
    "Mi Mineur": ["E", "F#", "G", "A", "B", "C", "D"],
    "Fa Mineur": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
    "Fa# Mineur": ["F#", "G#", "A", "B", "C#", "D", "E"],
    "Sol Mineur": ["G", "A", "Bb", "C", "D", "Eb", "F"],
    "Sol# Mineur": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
    "La Mineur": ["A", "B", "C", "D", "E", "F", "G"],
    "La# Mineur": ["A#", "B#", "C#", "D#", "E#", "F#", "G#"],
    "Si Mineur": ["B", "C#", "D", "E", "F#", "G", "A"],
}

# 2. PALETTES D'ACCORDS DIATONIQUES (7 accords pour chaque tonalité)
PALETTES = {
    # Tonalités majeures : I, ii, iii, IV, V, vi, vii°
    "Do Majeur": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
    "Do# Majeur": ["C#", "D#m", "E#m", "F#", "G#", "A#m", "B#dim"],
    "Ré Majeur": ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"],
    "Ré# Majeur": ["D#", "E#m", "F##m", "G#", "A#", "B#m", "C##dim"],
    "Mi Majeur": ["E", "F#m", "G#m", "A", "B", "C#m", "D#dim"],
    "Fa Majeur": ["F", "Gm", "Am", "Bb", "C", "Dm", "Edim"],
    "Fa# Majeur": ["F#", "G#m", "A#m", "B", "C#", "D#m", "E#dim"],
    "Sol Majeur": ["G", "Am", "Bm", "C", "D", "Em", "F#dim"],
    "Sol# Majeur": ["G#", "A#m", "B#m", "C#", "D#", "E#m", "F##dim"],
    "La Majeur": ["A", "Bm", "C#m", "D", "E", "F#m", "G#dim"],
    "La# Majeur": ["A#", "B#m", "C##m", "D#", "E#", "F##m", "G##dim"],
    "Si Majeur": ["B", "C#m", "D#m", "E", "F#", "G#m", "A#dim"],

    # Tonalités mineures : i, ii°, III, iv, v, VI, VII
    "Do Mineur": ["Cm", "Ddim", "Eb", "Fm", "Gm", "Ab", "Bb"],
    "Do# Mineur": ["C#m", "D#dim", "E", "F#m", "G#m", "A", "B"],
    "Ré Mineur": ["Dm", "Edim", "F", "Gm", "Am", "Bb", "C"],
    "Ré# Mineur": ["D#m", "E#dim", "F#", "G#m", "A#m", "B", "C#"],
    "Mi Mineur": ["Em", "F#dim", "G", "Am", "Bm", "C", "D"],
    "Fa Mineur": ["Fm", "Gdim", "Ab", "Bbm", "Cm", "Db", "Eb"],
    "Fa# Mineur": ["F#m", "G#dim", "A", "Bm", "C#m", "D", "E"],
    "Sol Mineur": ["Gm", "Adim", "Bb", "Cm", "Dm", "Eb", "F"],
    "Sol# Mineur": ["G#m", "A#dim", "B", "C#m", "D#m", "E", "F#"],
    "La Mineur": ["Am", "Bdim", "C", "Dm", "Em", "F", "G"],
    "La# Mineur": ["A#m", "B#dim", "C#", "D#m", "E#m", "F#", "G#"],
    "Si Mineur": ["Bm", "C#dim", "D", "Em", "F#m", "G", "A"],
}

# 3. FONCTIONS DES ACCORDS (par degré)
FONCTIONS_MAJEUR = {
    1: "Tonique",
    2: "Sous-dominante",
    3: "Tonique",
    4: "Sous-dominante",
    5: "Dominante",
    6: "Tonique",
    7: "Dominante",
}

FONCTIONS_MINEUR = {
    1: "Tonique",
    2: "Sous-dominante",
    3: "Tonique",
    4: "Sous-dominante",
    5: "Dominante",
    6: "Sous-dominante",
    7: "Dominante",
}

# 4. CONTENU DES ACCORDS (notes constitutives)
CONTENU_ACCORDS = {
    # Accords majeurs
    "C": ["C", "E", "G"],
    "C#": ["C#", "E#", "G#"],
    "D": ["D", "F#", "A"],
    "D#": ["D#", "F##", "A#"],
    "E": ["E", "G#", "B"],
    "F": ["F", "A", "C"],
    "F#": ["F#", "A#", "C#"],
    "G": ["G", "B", "D"],
    "G#": ["G#", "B#", "D#"],
    "A": ["A", "C#", "E"],
    "A#": ["A#", "C##", "E#"],
    "B": ["B", "D#", "F#"],
    "Bb": ["Bb", "D", "F"],
    "Eb": ["Eb", "G", "Bb"],
    "Ab": ["Ab", "C", "Eb"],
    "Db": ["Db", "F", "Ab"],

    # Accords mineurs
    "Cm": ["C", "Eb", "G"],
    "C#m": ["C#", "E", "G#"],
    "Dm": ["D", "F", "A"],
    "D#m": ["D#", "F#", "A#"],
    "Em": ["E", "G", "B"],
    "E#m": ["E#", "G#", "B#"],
    "Fm": ["F", "Ab", "C"],
    "F#m": ["F#", "A", "C#"],
    "F##m": ["F##", "A#", "C##"],
    "Gm": ["G", "Bb", "D"],
    "G#m": ["G#", "B", "D#"],
    "Am": ["A", "C", "E"],
    "A#m": ["A#", "C#", "E#"],
    "Bm": ["B", "D", "F#"],
    "B#m": ["B#", "D#", "F##"],
    "Bbm": ["Bb", "Db", "F"],
    "Ebm": ["Eb", "Gb", "Bb"],
    "Abm": ["Ab", "Cb", "Eb"],
    "C##m": ["C##", "E#", "G##"],

    # Accords diminués
    "Bdim": ["B", "D", "F"],
    "B#dim": ["B#", "D#", "F#"],
    "C#dim": ["C#", "E", "G"],
    "C##dim": ["C##", "E#", "G#"],
    "Ddim": ["D", "F", "Ab"],
    "D#dim": ["D#", "F#", "A"],
    "Edim": ["E", "G", "Bb"],
    "E#dim": ["E#", "G#", "B"],
    "F#dim": ["F#", "A", "C"],
    "F##dim": ["F##", "A#", "C#"],
    "Gdim": ["G", "Bb", "Db"],
    "G#dim": ["G#", "B", "D"],
    "G##dim": ["G##", "B#", "D#"],
    "Adim": ["A", "C", "Eb"],
    "A#dim": ["A#", "C#", "E"],
}

# Fonction helper pour normaliser les notes (enlever octaves)
def normaliser_note(note: str) -> str:
    """Enlève l'octave d'une note (ex: 'C4' -> 'C')"""
    return ''.join([c for c in note if not c.isdigit()])

def normaliser_note_enharmonique(note: str) -> str:
    """
    Normalise les équivalences enharmoniques pour la comparaison
    Ex: C# = Db, E# = F, etc.
    """
    equivalences = {
        "C#": "Db", "Db": "C#",
        "D#": "Eb", "Eb": "D#",
        "E#": "F", "Fb": "E",
        "F#": "Gb", "Gb": "F#",
        "G#": "Ab", "Ab": "G#",
        "A#": "Bb", "Bb": "A#",
        "B#": "C", "Cb": "B",
    }
    note_norm = normaliser_note(note)
    return equivalences.get(note_norm, note_norm)
