import json
import os
from datetime import datetime

# Chemin vers le dossier d'enregistrement
DOSSIER_AFFAIRES = os.path.join(os.path.dirname(__file__), "affaires")

# Création automatique du dossier si inexistant
if not os.path.exists(DOSSIER_AFFAIRES):
    os.makedirs(DOSSIER_AFFAIRES)


def sauvegarder_affaire(affaire_dict):
    """
    Enregistre une affaire dans un fichier JSON.

    Structure du fichier :
    data/affaires/affaire_20240215_103522.json
    """

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"affaire_{horodatage}.json"
    chemin = os.path.join(DOSSIER_AFFAIRES, nom_fichier)

    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(affaire_dict, f, ensure_ascii=False, indent=4)

    return chemin