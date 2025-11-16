"""
Moteur harmonique intelligent basé sur la théorie musicale
"""
from typing import Optional
from music_theory import (
    GAMMES, PALETTES, FONCTIONS_MAJEUR, FONCTIONS_MINEUR,
    CONTENU_ACCORDS, normaliser_note, normaliser_note_enharmonique
)


class HarmonyEngineV2:
    """Moteur harmonique avancé avec détection de tonalité et suggestions contextuelles"""

    def __init__(self):
        pass

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

        # Normaliser les notes (enlever octaves et doublons)
        notes_uniques = set(normaliser_note(note) for note in notes_a_analyser)

        # Calculer le score de compatibilité pour chaque tonalité
        scores = {}

        for tonalite, gamme in GAMMES.items():
            score = 0
            # Pondération musicale basée sur l'importance des degrés
            for note in notes_uniques:
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

                # Attribution des points selon le degré
                if degre is None:
                    # Note hors-gamme : 0 point
                    score += 0
                elif degre == 1:
                    # Tonique (Degré I) : +3 points
                    score += 3
                elif degre == 5:
                    # Dominante (Degré V) : +2 points
                    score += 2
                elif degre == 7:
                    # Sensible (Degré VII) : +2 points
                    score += 2
                else:
                    # Autres notes diatoniques (II, III, IV, VI) : +1 point
                    score += 1

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

    def suggerer_accords_pour_melodie(
        self,
        melodie: list[str],
        tonalite_choisie: Optional[str] = None,
        fenetre_tonalite: int = 6
    ) -> dict[str, any]:
        """
        Fonction principale pour suggérer des accords pour toute une mélodie.
        Réévalue la tonalité à chaque note avec une fenêtre glissante.

        Args:
            melodie: Liste des notes de la mélodie
            tonalite_choisie: Tonalité choisie par l'utilisateur (optionnel)
            fenetre_tonalite: Nombre de notes à considérer pour détecter la tonalité (défaut: 6)

        Returns:
            Dictionnaire avec tonalités détectées et suggestions par note (avec tonalité par note)
        """
        # Détecter les tonalités possibles sur toute la mélodie (pour info globale)
        tonalites_detectees_globales = self.detecter_tonalite(melodie)

        # Générer les suggestions pour chaque note
        suggestions_par_note = []
        accord_precedent = None

        for i, note in enumerate(melodie):
            # Réévaluer la tonalité avec une fenêtre glissante
            notes_precedentes = melodie[:i+1]  # Toutes les notes jusqu'à maintenant
            tonalites_locales = self.detecter_tonalite(notes_precedentes, fenetre=fenetre_tonalite)

            # Choisir la tonalité
            if tonalite_choisie:
                # L'utilisateur a forcé une tonalité
                tonalite_actuelle = tonalite_choisie
            elif tonalites_locales:
                # Prendre la tonalité la plus probable pour ce moment
                tonalite_actuelle = tonalites_locales[0]["tonalite"]
            else:
                # Fallback sur la tonalité globale
                tonalite_actuelle = tonalites_detectees_globales[0]["tonalite"] if tonalites_detectees_globales else "Do Majeur"
            # Générer les suggestions d'accords pour cette note avec la tonalité actuelle
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
                "detected_key": tonalite_actuelle,  # Tonalité détectée pour cette note
                "key_candidates": tonalites_locales[:3] if tonalites_locales else []  # Top 3 tonalités possibles
            })

            # L'accord "choisi" pour le contexte est le premier suggéré
            if chord_options:
                accord_precedent = chord_options[0]["name"]

        return {
            "detected_keys": tonalites_detectees_globales,
            "chosen_key": tonalite_choisie if tonalite_choisie else (tonalites_detectees_globales[0]["tonalite"] if tonalites_detectees_globales else "Do Majeur"),
            "suggestions": suggestions_par_note
        }
