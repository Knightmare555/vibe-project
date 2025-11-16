"""
Palette de couleurs pour les notes et tonalités musicales
"""
import colorsys
from music_theory import GAMMES, normaliser_note


def _generer_cycle_couleurs():
    """
    Génère un cycle de 12 couleurs vives et harmonieuses
    basé sur le cercle chromatique (HSL)
    """
    N = 12  # 12 notes chromatiques
    couleurs_hex = []

    # Saturation et luminosité fixes pour des couleurs vives
    saturation = 1.0
    luminosite = 0.5

    for i in range(N):
        # Teinte uniformément répartie sur le cercle chromatique
        teinte = i / N

        # Conversion HSL -> RGB
        (r, g, b) = colorsys.hls_to_rgb(teinte, luminosite, saturation)

        # Conversion RGB (0.0-1.0) -> Hexadécimal
        r_hex = int(r * 255)
        g_hex = int(g * 255)
        b_hex = int(b * 255)

        code_hex = f'#{r_hex:02x}{g_hex:02x}{b_hex:02x}'
        couleurs_hex.append(code_hex)

    return couleurs_hex


# Générer les couleurs une seule fois au chargement du module
_COULEURS = _generer_cycle_couleurs()

# Mapping notes -> couleurs (ordre chromatique: C, C#, D, D#, E, F, F#, G, G#, A, A#, B)
COULEURS_NOTES = {
    "C": _COULEURS[0],
    "C#": _COULEURS[1],
    "D": _COULEURS[2],
    "D#": _COULEURS[3],
    "E": _COULEURS[4],
    "F": _COULEURS[5],
    "F#": _COULEURS[6],
    "G": _COULEURS[7],
    "G#": _COULEURS[8],
    "A": _COULEURS[9],
    "A#": _COULEURS[10],
    "B": _COULEURS[11],
    # Équivalences enharmoniques
    "Db": _COULEURS[1],
    "Eb": _COULEURS[3],
    "Gb": _COULEURS[6],
    "Ab": _COULEURS[8],
    "Bb": _COULEURS[10],
}

# Mapping français -> anglais pour les notes
_NOTE_FR_TO_EN = {
    "Do": "C", "Do#": "C#",
    "Ré": "D", "Ré#": "D#",
    "Mi": "E",
    "Fa": "F", "Fa#": "F#",
    "Sol": "G", "Sol#": "G#",
    "La": "A", "La#": "A#",
    "Si": "B"
}

# Couleurs pour les tonalités (basées sur la note tonique)
COULEURS_TONALITES = {
    tonalite: COULEURS_NOTES.get(_NOTE_FR_TO_EN.get(tonalite.split()[0], ""), "#888888")
    for tonalite in GAMMES.keys()
}


def get_couleur_note(note: str) -> str:
    """
    Retourne la couleur hexadécimale associée à une note.

    Args:
        note: Note avec ou sans octave (ex: "C", "C4", "C#")

    Returns:
        Code couleur hexadécimal (ex: "#ff0000")
    """
    note_norm = normaliser_note(note)
    return COULEURS_NOTES.get(note_norm, "#888888")  # Gris par défaut


def get_couleur_tonalite(tonalite: str) -> str:
    """
    Retourne la couleur hexadécimale associée à une tonalité.

    Args:
        tonalite: Tonalité (ex: "Do Majeur", "La Mineur")

    Returns:
        Code couleur hexadécimal (ex: "#ff0000")
    """
    return COULEURS_TONALITES.get(tonalite, "#888888")  # Gris par défaut
