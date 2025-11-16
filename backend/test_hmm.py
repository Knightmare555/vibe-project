"""
Script de test pour le modèle de Markov caché (HMM)
"""
from harmony_engine import HarmonyEngine

def test_hmm():
    engine = HarmonyEngine()

    print("=" * 60)
    print("TEST DU MODÈLE DE MARKOV CACHÉ (HMM)")
    print("=" * 60)

    # Test 1: Mélodie en Do Majeur (C D E F G)
    print("\n--- Test 1: Gamme de Do Majeur ---")
    melodie_c_major = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]

    # Ancienne méthode
    result_old = engine.detecter_tonalite(melodie_c_major)
    print(f"Ancienne méthode: {result_old[0]['tonalite']} (score: {result_old[0]['score']})")

    # Nouvelle méthode HMM
    result_hmm = engine.detecter_tonalite_hmm(melodie_c_major)
    print(f"Nouvelle méthode HMM: {result_hmm[0]['tonalite']}")

    # Séquence complète
    sequence = engine.detecter_tonalite_sequence(melodie_c_major)
    print("\nSéquence de tonalités détectées:")
    for i, item in enumerate(sequence):
        print(f"  {i+1}. {item['note']} -> {item['tonalite']} (prob: {item['probabilite']:.6f})")

    # Test 2: Mélodie en La mineur (A B C D E)
    print("\n--- Test 2: Gamme de La mineur ---")
    melodie_a_minor = ["A3", "B3", "C4", "D4", "E4", "F4", "G4", "A4"]

    result_old = engine.detecter_tonalite(melodie_a_minor)
    print(f"Ancienne méthode: {result_old[0]['tonalite']} (score: {result_old[0]['score']})")

    result_hmm = engine.detecter_tonalite_hmm(melodie_a_minor)
    print(f"Nouvelle méthode HMM: {result_hmm[0]['tonalite']}")

    sequence = engine.detecter_tonalite_sequence(melodie_a_minor)
    print("\nSéquence de tonalités détectées:")
    for i, item in enumerate(sequence):
        print(f"  {i+1}. {item['note']} -> {item['tonalite']} (prob: {item['probabilite']:.6f})")

    # Test 3: Modulation de Do Majeur à Sol Majeur
    print("\n--- Test 3: Modulation Do Majeur -> Sol Majeur ---")
    melodie_modulation = [
        "C4", "E4", "G4", "C5",  # Do Majeur
        "D4", "F#4", "A4", "D5"  # Sol Majeur (F# est la note caractéristique)
    ]

    result_old = engine.detecter_tonalite(melodie_modulation)
    print(f"Ancienne méthode (globale): {result_old[0]['tonalite']} (score: {result_old[0]['score']})")

    result_hmm = engine.detecter_tonalite_hmm(melodie_modulation)
    print(f"Nouvelle méthode HMM (globale): {result_hmm[0]['tonalite']}")

    sequence = engine.detecter_tonalite_sequence(melodie_modulation)
    print("\nSéquence de tonalités détectées (devrait montrer la modulation):")
    for i, item in enumerate(sequence):
        print(f"  {i+1}. {item['note']} -> {item['tonalite']} (prob: {item['probabilite']:.6f})")

    # Test 4: Fenêtre glissante
    print("\n--- Test 4: Détection avec fenêtre glissante ---")
    melodie_longue = ["C4", "E4", "G4", "C5", "D4", "F#4", "A4", "D5", "B4", "D5", "G5"]

    print("Fenêtre de 4 notes:")
    for i in range(4, len(melodie_longue) + 1):
        result_window = engine.detecter_tonalite_hmm(melodie_longue[:i], fenetre=4)
        print(f"  Notes {i-3} à {i}: {result_window[0]['tonalite']}")

    print("\n" + "=" * 60)
    print("TESTS TERMINÉS")
    print("=" * 60)

if __name__ == "__main__":
    test_hmm()
