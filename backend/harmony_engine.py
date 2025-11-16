"""
Moteur harmonique intelligent basé sur la théorie musicale
"""
from typing import Optional
import numpy as np
from music_theory import (
    GAMMES, PALETTES, FONCTIONS_MAJEUR, FONCTIONS_MINEUR,
    CONTENU_ACCORDS, normaliser_note, normaliser_note_enharmonique
)


class HiddenMarkovModel:
    """
    Modèle de Markov Caché pour la détection de tonalité.

    États cachés: 24 tonalités (12 majeures + 12 mineures)
    Observations: 12 notes (C, C#, D, D#, E, F, F#, G, G#, A, A#, B)
    """

    def __init__(self):
        # Mapping français -> anglais pour les notes
        self.note_mapping = {
            "Do": "C", "Do#": "C#",
            "Ré": "D", "Ré#": "D#",
            "Mi": "E",
            "Fa": "F", "Fa#": "F#",
            "Sol": "G", "Sol#": "G#",
            "La": "A", "La#": "A#",
            "Si": "B"
        }

        # Liste des tonalités (états cachés)
        self.tonalites = list(GAMMES.keys())
        self.n_states = len(self.tonalites)  # 24

        # Liste des notes (observations)
        self.notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.n_observations = len(self.notes)  # 12

        # Mapping pour accès rapide
        self.tonalite_to_idx = {t: i for i, t in enumerate(self.tonalites)}
        self.note_to_idx = {n: i for i, n in enumerate(self.notes)}

        # Construire les matrices
        self.transition_matrix = self._build_transition_matrix()
        self.emission_matrix = self._build_emission_matrix()
        self.initial_probabilities = self._build_initial_probabilities()

    def _tonalite_to_english_note(self, tonalite: str) -> str:
        """Extrait la note tonique d'une tonalité et la convertit en notation anglaise."""
        # Extraire la partie note (avant " Majeur" ou " Mineur")
        note_fr = tonalite.split()[0]
        return self.note_mapping.get(note_fr, note_fr)

    def _get_circle_of_fifths_distance(self, note1: str, note2: str) -> int:
        """Calcule la distance sur le cycle des quintes entre deux notes."""
        # Cycle des quintes: C G D A E B F# C# G# D# A# F C
        circle = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]

        try:
            idx1 = circle.index(note1)
            idx2 = circle.index(note2)
            # Distance minimale (circulaire)
            dist = min(abs(idx2 - idx1), 12 - abs(idx2 - idx1))
            return dist
        except ValueError:
            return 6  # Maximum distance si note pas trouvée

    def _are_relative_keys(self, ton1: str, ton2: str) -> bool:
        """Vérifie si deux tonalités sont relatives (ex: Do Majeur et La mineur)."""
        # Extraire la note tonique de chaque tonalité et convertir en notation anglaise
        note1 = self._tonalite_to_english_note(ton1)
        note2 = self._tonalite_to_english_note(ton2)

        # Une tonalité doit être majeure et l'autre mineure
        is_major1 = "Majeur" in ton1
        is_major2 = "Majeur" in ton2

        if is_major1 == is_major2:
            return False

        # Vérifier la relation de tierce mineure (3 demi-tons)
        # Do Majeur -> La mineur (descente de 3 demi-tons)
        idx1 = self.notes.index(note1)
        idx2 = self.notes.index(note2)

        if is_major1:
            # Majeur -> mineur relatif: descente de 3 demi-tons
            return (idx1 - 3) % 12 == idx2
        else:
            # mineur -> Majeur relatif: montée de 3 demi-tons
            return (idx1 + 3) % 12 == idx2

    def _build_transition_matrix(self) -> np.ndarray:
        """
        Construit la matrice de transition 24x24.

        Probabilités basées sur le cycle des quintes:
        - Rester sur place: 0.90
        - Quinte (distance 1): 0.03
        - Quarte (distance 1 dans l'autre sens): 0.03
        - Relatif mineur/majeur: 0.02
        - Autres: ~0.0001
        """
        matrix = np.zeros((self.n_states, self.n_states))

        for i, ton1 in enumerate(self.tonalites):
            note1 = self._tonalite_to_english_note(ton1)
            total_prob = 0.0

            for j, ton2 in enumerate(self.tonalites):
                note2 = self._tonalite_to_english_note(ton2)

                if i == j:
                    # Rester sur la même tonalité
                    prob = 0.90
                elif self._are_relative_keys(ton1, ton2):
                    # Transition vers le relatif
                    prob = 0.02
                else:
                    # Basé sur le cycle des quintes
                    distance = self._get_circle_of_fifths_distance(note1, note2)

                    if distance == 1:
                        # Quinte ou Quarte
                        prob = 0.03
                    elif distance == 2:
                        prob = 0.005
                    elif distance == 6:
                        # Triton (opposé)
                        prob = 0.0001
                    else:
                        prob = 0.001

                matrix[i, j] = prob
                total_prob += prob

            # Normaliser pour que la somme fasse 1
            if total_prob > 0:
                matrix[i, :] /= total_prob

        return matrix

    def _build_emission_matrix(self) -> np.ndarray:
        """
        Construit la matrice d'émission 24x12.

        P(note | tonalité) basé sur le scoring actuel:
        - Tonique (degré I): haute probabilité
        - Dominante (degré V): moyenne-haute
        - Sensible (degré VII): moyenne-haute
        - Autres notes de la gamme: moyenne
        - Notes hors gamme: très faible
        """
        matrix = np.zeros((self.n_states, self.n_observations))

        for i, tonalite in enumerate(self.tonalites):
            gamme = GAMMES[tonalite]

            for j, note in enumerate(self.notes):
                # Normaliser la note
                note_norm = normaliser_note(note)

                # Trouver le degré
                degre = None
                if note_norm in gamme:
                    degre = gamme.index(note_norm) + 1
                else:
                    # Équivalence enharmonique
                    note_equiv = normaliser_note_enharmonique(note_norm)
                    if note_equiv in gamme:
                        degre = gamme.index(note_equiv) + 1

                # Attribution des probabilités selon le degré
                if degre is None:
                    # Note hors gamme: très faible probabilité
                    prob = 0.01
                elif degre == 1:
                    # Tonique: haute probabilité
                    prob = 0.25
                elif degre == 5:
                    # Dominante: moyenne-haute
                    prob = 0.20
                elif degre == 7:
                    # Sensible: moyenne-haute
                    prob = 0.15
                else:
                    # Autres notes diatoniques
                    prob = 0.10

                matrix[i, j] = prob

            # Normaliser pour que la somme fasse 1
            total = matrix[i, :].sum()
            if total > 0:
                matrix[i, :] /= total

        return matrix

    def _build_initial_probabilities(self) -> np.ndarray:
        """
        Construit les probabilités initiales (équiprobables pour commencer).
        """
        # On peut favoriser certaines tonalités (Do Majeur, La mineur, etc.)
        # Pour l'instant, on met une distribution uniforme
        probs = np.ones(self.n_states) / self.n_states
        return probs

    def viterbi(self, observations: list[str]) -> tuple[list[str], list[float]]:
        """
        Algorithme de Viterbi pour trouver la séquence de tonalités la plus probable.

        Args:
            observations: Liste de notes observées (ex: ["C", "E", "G", "F"])

        Returns:
            - path: Liste des tonalités les plus probables pour chaque note
            - probabilities: Probabilités associées
        """
        T = len(observations)

        # Matrices de calcul
        delta = np.zeros((T, self.n_states))  # Probabilités max
        psi = np.zeros((T, self.n_states), dtype=int)  # Chemins

        # Convertir les observations en indices
        obs_indices = []
        for obs in observations:
            obs_norm = normaliser_note(obs)
            if obs_norm in self.note_to_idx:
                obs_indices.append(self.note_to_idx[obs_norm])
            else:
                # Note enharmonique
                obs_equiv = normaliser_note_enharmonique(obs_norm)
                if obs_equiv in self.note_to_idx:
                    obs_indices.append(self.note_to_idx[obs_equiv])
                else:
                    # Fallback sur C si note inconnue
                    obs_indices.append(0)

        # Initialisation (t=0)
        obs_0 = obs_indices[0]
        delta[0, :] = self.initial_probabilities * self.emission_matrix[:, obs_0]

        # Récurrence (t=1 à T-1)
        for t in range(1, T):
            obs_t = obs_indices[t]

            for j in range(self.n_states):
                # Calculer le max sur tous les états précédents
                probs = delta[t-1, :] * self.transition_matrix[:, j] * self.emission_matrix[j, obs_t]
                delta[t, j] = np.max(probs)
                psi[t, j] = np.argmax(probs)

        # Terminaison - trouver le meilleur état final
        path_indices = np.zeros(T, dtype=int)
        path_indices[-1] = np.argmax(delta[-1, :])

        # Backtracking
        for t in range(T-2, -1, -1):
            path_indices[t] = psi[t+1, path_indices[t+1]]

        # Convertir les indices en tonalités
        path = [self.tonalites[idx] for idx in path_indices]

        # Récupérer les probabilités
        probabilities = [delta[t, path_indices[t]] for t in range(T)]

        return path, probabilities


class HarmonyEngine:
    """Moteur harmonique avancé avec détection de tonalité et suggestions contextuelles"""

    def __init__(self):
        self.hmm = HiddenMarkovModel()

    def detecter_tonalite(self, liste_notes: list[str], fenetre: Optional[int] = None) -> list[dict[str, any]]:
        """
        ALGORITHME 1: Détecteur de Tonalité

        Analyse une liste de notes et retourne les 3 tonalités les plus probables.

        Args:
            liste_notes: Liste des notes de la mélodie (ex: ["C4", "E4", "G4"])
            fenetre: Si spécifié, n'analyse que les N dernières notes (fenêtre glissante)

        Returns:
            Liste des 3 tonalités avec scores (ex: [{"tonalite": "Do Majeur", "score": 6}, ...])
        """
        if not liste_notes:
            return []

        # Appliquer la fenêtre glissante si spécifiée
        notes_a_analyser = liste_notes
        if fenetre is not None and fenetre > 0:
            notes_a_analyser = liste_notes[-fenetre:]

        # Normaliser les notes (enlever octaves) et compter les occurrences
        from collections import Counter
        notes_comptees = Counter(normaliser_note(note) for note in notes_a_analyser)

        # Calculer le score de compatibilité pour chaque tonalité
        scores = {}

        for tonalite, gamme in GAMMES.items():
            score = 0
            # Pondération musicale basée sur l'importance des degrés
            for note, frequence in notes_comptees.items():
                note_norm = normaliser_note(note)

                # Trouver le degré de la note dans cette gamme
                degre = None
                if note_norm in gamme:
                    degre = gamme.index(note_norm) + 1  # Degrés de 1 à 7
                else:
                    # Vérifier avec équivalence enharmonique
                    note_equiv = normaliser_note_enharmonique(note_norm)
                    if note_equiv in gamme:
                        degre = gamme.index(note_equiv) + 1

                # Attribution des points selon le degré (multiplié par la fréquence)
                points = 0
                if degre is None:
                    # Note hors-gamme : 0 point
                    points = 0
                elif degre == 1:
                    # Tonique (Degré I) : +3 points
                    points = 3
                elif degre == 5:
                    # Dominante (Degré V) : +2 points
                    points = 2
                elif degre == 7:
                    # Sensible (Degré VII) : +2 points
                    points = 2
                else:
                    # Autres notes diatoniques (II, III, IV, VI) : +1 point
                    points = 1

                score += points * frequence

            scores[tonalite] = score

        # Trier par score décroissant et prendre les 3 meilleures
        tonalites_triees = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        # Formater le résultat
        resultat = [
            {"tonalite": tonalite, "score": score}
            for tonalite, score in tonalites_triees
        ]

        return resultat

    def detecter_tonalite_hmm(self, liste_notes: list[str], fenetre: Optional[int] = None) -> list[dict[str, any]]:
        """
        ALGORITHME 1 (HMM): Détecteur de Tonalité avec Modèle de Markov Caché

        Analyse une liste de notes et retourne les tonalités les plus probables
        en utilisant l'algorithme de Viterbi sur un HMM.

        Args:
            liste_notes: Liste des notes de la mélodie (ex: ["C4", "E4", "G4"])
            fenetre: Si spécifié, n'analyse que les N dernières notes (fenêtre glissante)

        Returns:
            Liste des tonalités avec scores pour chaque note
        """
        if not liste_notes:
            return []

        # Appliquer la fenêtre glissante si spécifiée
        notes_a_analyser = liste_notes
        if fenetre is not None and fenetre > 0:
            notes_a_analyser = liste_notes[-fenetre:]

        # Utiliser Viterbi pour trouver la séquence optimale
        path, probabilities = self.hmm.viterbi(notes_a_analyser)

        # Si on utilise une fenêtre, on ne retourne que la dernière tonalité détectée
        if fenetre is not None:
            tonalite_actuelle = path[-1]
            prob_actuelle = probabilities[-1]

            # Convertir en log-probabilité
            log_prob = float(np.log(prob_actuelle)) if prob_actuelle > 0 else float(-np.inf)

            # Retourner les 3 meilleures tonalités pour l'instant actuel
            # (pour compatibilité avec l'API existante)
            # On pourrait améliorer en calculant les probabilités pour toutes les tonalités
            return [{"tonalite": tonalite_actuelle, "score": log_prob}]
        else:
            # Retourner la séquence complète de tonalités
            from collections import Counter
            # Compter les tonalités les plus fréquentes dans le path
            tonalite_counts = Counter(path)
            top_tonalites = tonalite_counts.most_common(3)

            return [
                {"tonalite": tonalite, "score": count}
                for tonalite, count in top_tonalites
            ]

    def detecter_tonalite_sequence(self, liste_notes: list[str]) -> list[dict[str, any]]:
        """
        Détecte la séquence de tonalités pour chaque note de la mélodie.

        Args:
            liste_notes: Liste des notes de la mélodie

        Returns:
            Liste de dictionnaires avec la tonalité et la log-probabilité pour chaque note
        """
        if not liste_notes:
            return []

        # Utiliser Viterbi pour obtenir la séquence complète
        path, probabilities = self.hmm.viterbi(liste_notes)

        # Retourner la tonalité pour chaque note avec log-probabilités
        return [
            {
                "note": note,
                "tonalite": tonalite,
                "log_probabilite": float(np.log(prob)) if prob > 0 else float(-np.inf)
            }
            for note, tonalite, prob in zip(liste_notes, path, probabilities)
        ]

    def _get_degree_of_note(self, note: str, tonalite: str) -> Optional[int]:
        """
        Trouve le degré d'une note dans une tonalité donnée.

        Args:
            note: La note (ex: "A")
            tonalite: La tonalité (ex: "Sol Majeur")

        Returns:
            Le degré (1-7) ou None si la note n'est pas dans la gamme
        """
        gamme = GAMMES.get(tonalite)
        if not gamme:
            return None

        note_norm = normaliser_note(note)

        # Chercher la note directement
        if note_norm in gamme:
            return gamme.index(note_norm) + 1  # Degrés commencent à 1

        # Chercher avec équivalence enharmonique
        note_equiv = normaliser_note_enharmonique(note_norm)
        if note_equiv in gamme:
            return gamme.index(note_equiv) + 1

        return None

    def _get_fonction(self, degre: int, tonalite: str) -> str:
        """
        Retourne la fonction d'un degré dans une tonalité.

        Args:
            degre: Le degré (1-7)
            tonalite: La tonalité

        Returns:
            La fonction ("Tonique", "Dominante", "Sous-dominante")
        """
        is_major = "Majeur" in tonalite
        fonctions = FONCTIONS_MAJEUR if is_major else FONCTIONS_MINEUR
        return fonctions.get(degre, "Inconnu")

    def _get_accords_by_fonction(self, fonction: str, tonalite: str) -> list[str]:
        """
        Retourne tous les accords d'une palette qui ont une fonction donnée.

        Args:
            fonction: La fonction recherchée
            tonalite: La tonalité

        Returns:
            Liste des accords ayant cette fonction
        """
        palette = PALETTES.get(tonalite, [])
        is_major = "Majeur" in tonalite
        fonctions = FONCTIONS_MAJEUR if is_major else FONCTIONS_MINEUR

        accords = []
        for degre, func in fonctions.items():
            if func == fonction and 1 <= degre <= len(palette):
                accords.append(palette[degre - 1])

        return accords

    def _accord_contient_note(self, accord: str, note: str) -> bool:
        """Vérifie si un accord contient une note"""
        notes_accord = CONTENU_ACCORDS.get(accord, [])
        note_norm = normaliser_note(note)

        # Vérification directe
        if note_norm in notes_accord:
            return True

        # Vérification avec équivalence enharmonique
        note_equiv = normaliser_note_enharmonique(note_norm)
        return note_equiv in notes_accord

    def suggerer_accords(
        self,
        note_actuelle: str,
        tonalite_choisie: str,
        accord_precedent: Optional[str] = None
    ) -> list[dict[str, any]]:
        """
        ALGORITHME 2: Moteur de Suggestion

        Génère des suggestions d'accords intelligentes basées sur le contexte.

        Args:
            note_actuelle: La note sur laquelle l'utilisateur clique (ex: "A")
            tonalite_choisie: La tonalité choisie (ex: "Sol Majeur")
            accord_precedent: L'accord joué juste avant (optionnel)

        Returns:
            Liste d'accords suggérés avec raisons, triée par pertinence
        """
        suggestions = []
        palette = PALETTES.get(tonalite_choisie, [])

        if not palette:
            return []

        # Trouver le degré de la note actuelle
        degre = self._get_degree_of_note(note_actuelle, tonalite_choisie)

        if degre is None:
            # La note n'est pas dans la gamme, suggérer les accords qui la contiennent
            for accord in palette:
                if self._accord_contient_note(accord, note_actuelle):
                    suggestions.append({
                        "accord": accord,
                        "priorite": 4,
                        "raison": "Accord hors gamme contenant cette note"
                    })
            return sorted(suggestions, key=lambda x: x["priorite"])

        # PRIORITÉ 1: Accord du degré
        if 1 <= degre <= len(palette):
            accord_degre = palette[degre - 1]
            fonction = self._get_fonction(degre, tonalite_choisie)
            suggestions.append({
                "accord": accord_degre,
                "priorite": 1,
                "raison": f"Accord du degré {degre} ({fonction})"
            })

        # PRIORITÉ 2: Autres accords de même fonction
        fonction_note = self._get_fonction(degre, tonalite_choisie)
        accords_meme_fonction = self._get_accords_by_fonction(fonction_note, tonalite_choisie)

        for accord in accords_meme_fonction:
            if accord != palette[degre - 1]:  # Exclure l'accord déjà ajouté en priorité 1
                suggestions.append({
                    "accord": accord,
                    "priorite": 2,
                    "raison": f"Autre accord de {fonction_note}"
                })

        # PRIORITÉ 3: Résolution harmonique (si accord précédent est Dominante)
        if accord_precedent:
            # Trouver le degré de l'accord précédent
            try:
                degre_precedent = palette.index(accord_precedent) + 1
                fonction_precedent = self._get_fonction(degre_precedent, tonalite_choisie)

                if fonction_precedent == "Dominante":
                    # Suggérer les Toniques
                    accords_toniques = self._get_accords_by_fonction("Tonique", tonalite_choisie)
                    for accord in accords_toniques:
                        if self._accord_contient_note(accord, note_actuelle):
                            # Vérifier si pas déjà dans les suggestions
                            if not any(s["accord"] == accord for s in suggestions):
                                suggestions.append({
                                    "accord": accord,
                                    "priorite": 3,
                                    "raison": "Résolution de Dominante vers Tonique"
                                })
            except ValueError:
                pass  # L'accord précédent n'est pas dans la palette

        # PRIORITÉ 4: Compatibilité simple (autres accords contenant la note)
        for accord in palette:
            if self._accord_contient_note(accord, note_actuelle):
                # Vérifier si pas déjà dans les suggestions
                if not any(s["accord"] == accord for s in suggestions):
                    suggestions.append({
                        "accord": accord,
                        "priorite": 4,
                        "raison": "Contient cette note"
                    })

        # Trier par priorité (plus petit = plus prioritaire)
        suggestions_triees = sorted(suggestions, key=lambda x: x["priorite"])

        return suggestions_triees

    def detecter_tonalite_melodie(
        self,
        melodie: list[str],
        tonalite_choisie: Optional[str] = None,
        fenetre_tonalite: int = 6,
        algorithm: str = "hmm"
    ) -> dict[str, any]:
        """
        Détecte les tonalités pour une mélodie (globale et locale par note).

        Args:
            melodie: Liste des notes de la mélodie
            tonalite_choisie: Tonalité forcée par l'utilisateur (optionnel)
            fenetre_tonalite: Taille de la fenêtre glissante (utilisée uniquement pour scoring)
            algorithm: "hmm" ou "scoring"

        Returns:
            Dictionnaire contenant:
            - tonalites_globales: Top 3 tonalités pour toute la mélodie
            - tonalites_par_note: Liste de dict avec tonalité détectée pour chaque note
            - tonalite_choisie: Tonalité finale choisie
        """
        if not melodie:
            return {
                "tonalites_globales": [],
                "tonalites_par_note": [],
                "tonalite_choisie": "Do Majeur"
            }

        if algorithm == "hmm":
            # HMM : Viterbi calcule le chemin optimal sur toute la séquence
            # Pas besoin de fenêtre glissante, on calcule tout d'un coup

            # 1. Calculer le path de Viterbi UNE SEULE FOIS
            path, probabilities = self.hmm.viterbi(melodie)

            # 2. Estimer les tonalités globales à partir du path de Viterbi
            from collections import Counter
            tonalite_counts = Counter(path)
            top_tonalites = tonalite_counts.most_common(3)

            tonalites_globales = [
                {"tonalite": tonalite, "score": count}
                for tonalite, count in top_tonalites
            ]

            # 3. Construire tonalites_par_note à partir du path de Viterbi
            tonalites_par_note = []
            for i, (note, tonalite, prob) in enumerate(zip(melodie, path, probabilities)):
                if tonalite_choisie:
                    tonalite_actuelle = tonalite_choisie
                else:
                    tonalite_actuelle = tonalite

                # Convertir en log-probabilité pour plus de lisibilité
                log_prob = np.log(prob) if prob > 0 else -np.inf

                tonalites_par_note.append({
                    "note": note,
                    "tonalite": tonalite_actuelle,
                    "tonalites_candidates": [{"tonalite": tonalite, "score": float(log_prob)}]
                })

        else:
            # SCORING : Algorithme stateless, la fenêtre glissante fait sens

            # Détecter les tonalités globales
            tonalites_globales = self.detecter_tonalite(melodie)

            # Détecter la tonalité locale pour chaque note avec fenêtre glissante
            tonalites_par_note = []
            for i, note in enumerate(melodie):
                notes_precedentes = melodie[:i+1]
                tonalites_locales = self.detecter_tonalite(notes_precedentes, fenetre=fenetre_tonalite)

                # Choisir la tonalité pour cette note
                if tonalite_choisie:
                    tonalite_actuelle = tonalite_choisie
                elif tonalites_locales:
                    tonalite_actuelle = tonalites_locales[0]["tonalite"]
                else:
                    tonalite_actuelle = tonalites_globales[0]["tonalite"] if tonalites_globales else "Do Majeur"

                tonalites_par_note.append({
                    "note": note,
                    "tonalite": tonalite_actuelle,
                    "tonalites_candidates": tonalites_locales[:3] if tonalites_locales else []
                })

        # Tonalité finale choisie
        tonalite_finale = tonalite_choisie if tonalite_choisie else (
            tonalites_globales[0]["tonalite"] if tonalites_globales else "Do Majeur"
        )

        return {
            "tonalites_globales": tonalites_globales,
            "tonalites_par_note": tonalites_par_note,
            "tonalite_choisie": tonalite_finale
        }

    def suggerer_accords_tonalite(
        self,
        melodie: list[str],
        tonalites_par_note: list[dict[str, any]]
    ) -> list[dict[str, any]]:
        """
        Suggère des accords pour chaque note d'une mélodie basé sur les tonalités détectées.

        Args:
            melodie: Liste des notes de la mélodie
            tonalites_par_note: Liste de dict avec tonalité pour chaque note

        Returns:
            Liste de suggestions d'accords formatées pour l'API
        """
        suggestions_par_note = []
        accord_precedent = None

        for i, note in enumerate(melodie):
            tonalite_info = tonalites_par_note[i]
            tonalite_actuelle = tonalite_info["tonalite"]

            # Générer les suggestions d'accords pour cette note
            suggestions = self.suggerer_accords(
                note,
                tonalite_actuelle,
                accord_precedent
            )

            # Prendre les 2 meilleures suggestions
            top_suggestions = suggestions[:2]

            # Formater pour l'API
            chord_options = []
            for sugg in top_suggestions:
                accord_nom = sugg["accord"]
                notes_accord = CONTENU_ACCORDS.get(accord_nom, [])

                # Déterminer la qualité
                if "m" in accord_nom and "dim" not in accord_nom:
                    quality = "minor"
                elif "dim" in accord_nom:
                    quality = "diminished"
                else:
                    quality = "major"

                chord_options.append({
                    "name": accord_nom,
                    "notes": notes_accord,
                    "quality": quality,
                    "reason": sugg["raison"]
                })

            suggestions_par_note.append({
                "note": note,
                "chord_options": chord_options,
                "detected_key": tonalite_actuelle,
                "key_candidates": tonalite_info["tonalites_candidates"]
            })

            # L'accord "choisi" pour le contexte est le premier suggéré
            if chord_options:
                accord_precedent = chord_options[0]["name"]

        return suggestions_par_note

    def suggerer_accords_pour_melodie(
        self,
        melodie: list[str],
        tonalite_choisie: Optional[str] = None,
        fenetre_tonalite: int = 6,
        algorithm: str = "hmm"
    ) -> dict[str, any]:
        """
        Fonction principale pour suggérer des accords pour toute une mélodie.
        Réévalue la tonalité à chaque note avec une fenêtre glissante.

        Cette fonction orchestre les deux étapes:
        1. Détection des tonalités (detecter_tonalite_melodie)
        2. Suggestion des accords (suggerer_accords_tonalite)

        Args:
            melodie: Liste des notes de la mélodie
            tonalite_choisie: Tonalité choisie par l'utilisateur (optionnel)
            fenetre_tonalite: Nombre de notes à considérer pour détecter la tonalité (défaut: 6)
            algorithm: Algorithme à utiliser ("scoring" ou "hmm", défaut: "hmm")

        Returns:
            Dictionnaire avec tonalités détectées et suggestions par note (avec tonalité par note)
        """
        # Étape 1: Détecter les tonalités
        tonalites_result = self.detecter_tonalite_melodie(
            melodie=melodie,
            tonalite_choisie=tonalite_choisie,
            fenetre_tonalite=fenetre_tonalite,
            algorithm=algorithm
        )

        # Étape 2: Suggérer les accords basés sur les tonalités détectées
        suggestions = self.suggerer_accords_tonalite(
            melodie=melodie,
            tonalites_par_note=tonalites_result["tonalites_par_note"]
        )

        # Retourner le résultat final
        return {
            "detected_keys": tonalites_result["tonalites_globales"],
            "chosen_key": tonalites_result["tonalite_choisie"],
            "suggestions": suggestions
        }
