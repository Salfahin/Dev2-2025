from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Personne:
    """
    Représente une personne impliquée dans une affaire.
    """
    role: str
    nom: str
    identité: str = ""
    adresse: str = ""
    contact: str = ""
    liens: str = ""
    historique: str = ""

    @staticmethod
    def from_dict(data: Dict) -> "Personne":
        """
        Construit une Personne à partir d'un dictionnaire JSON.
        """
        return Personne(
            role=data.get("role", ""),
            nom=data.get("nom", ""),
            identité=data.get("identité", ""),
            adresse=data.get("adresse", ""),
            contact=data.get("contact", ""),
            liens=data.get("liens", ""),
            historique=data.get("historique", "")
        )

    def to_dict(self) -> Dict:
        """
        Convertit la Personne en dictionnaire JSON.
        """
        return {
            "role": self.role,
            "nom": self.nom,
            "identité": self.identité,
            "adresse": self.adresse,
            "contact": self.contact,
            "liens": self.liens,
            "historique": self.historique
        }
