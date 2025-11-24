import os
import json
from datetime import datetime

AFFAIRES_PATH = "data/affaires"


def charger_affaires():
    affaires = []

    for fichier in os.listdir(AFFAIRES_PATH):
        if not fichier.endswith(".json"):
            continue

        chemin = os.path.join(AFFAIRES_PATH, fichier)

        with open(chemin, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Ajouter automatiquement la date de création si absente
        if "creation_time" not in data:
            data["creation_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(chemin, "w", encoding="utf-8") as fw:
                json.dump(data, fw, indent=4, ensure_ascii=False)

        # Comptage des personnes
        victimes = sum(1 for p in data.get("personnes", []) if "Victime" in p["role"])
        suspects = sum(1 for p in data.get("personnes", []) if "Suspect" in p["role"])
        temoins = sum(1 for p in data.get("personnes", []) if "témo" in p["role"].lower())

        affaire = {
            "titre": data.get("titre", ""),
            "lieu": data.get("lieu", ""),
            "date_dernier_mouvement": data.get("creation_time", ""),
            "type_affaire": data.get("type_affaire", ""),
            "responsable": data.get("responsables", ""),
            "etat": data.get("etat", "🟤 Gelée"),
            "victimes": victimes,
            "suspects": suspects,
            "temoins": temoins,
            "path": chemin
        }

        affaires.append(affaire)

    return affaires


def trier_par_etat(affaires):
    en_cours = [a for a in affaires if "En cours" in a["etat"]]
    surveiller = [a for a in affaires if "surveiller" in a["etat"].lower()]
    gelee = [a for a in affaires if "gel" in a["etat"].lower()]

    return en_cours, surveiller, gelee