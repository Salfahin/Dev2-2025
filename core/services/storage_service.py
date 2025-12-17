from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from core.interfaces.storage_interface import StorageInterface


class StorageService(StorageInterface):
    """
    Implémentation concrète du stockage des affaires au format JSON.
    """

    def __init__(self, base_path: str):
        self.base_path = base_path

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    # -----------------------------------------------------------
    #   LISTER LES FICHIERS
    # -----------------------------------------------------------
    def list_files(self) -> List[str]:
        return [
            f for f in os.listdir(self.base_path)
            if f.endswith(".json")
        ]

    # -----------------------------------------------------------
    #   SAUVEGARDER
    # -----------------------------------------------------------
    def save(self, data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Sauvegarde un dictionnaire en JSON.
        Si filename n'existe pas, un nom unique est généré.
        """

        if filename is None:
            horodatage = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"affaire_{horodatage}.json"

        full_path = os.path.join(self.base_path, filename)

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return full_path

    # -----------------------------------------------------------
    #   CHARGER UN FICHIER
    # -----------------------------------------------------------
    def load(self, filename: str) -> Dict[str, Any]:
        full_path = os.path.join(self.base_path, filename)

        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------------------------------------
    #   SUPPRIMER
    # -----------------------------------------------------------
    def delete(self, filename: str) -> None:
        full_path = os.path.join(self.base_path, filename)

        if os.path.exists(full_path):
            os.remove(full_path)

    # -----------------------------------------------------------
    #   CHARGER TOUS LES FICHIERS
    # -----------------------------------------------------------
    def load_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Charge tous les fichiers JSON et retourne un dictionnaire :
        {
            "affaire_20240101.json": { ... },
            "affaire_20240202.json": { ... }
        }
        """
        result = {}
        for filename in self.list_files():
            result[filename] = self.load(filename)
        return result
