from __future__ import annotations
from dataclasses import dataclass
from typing import Dict


@dataclass(init=False)
class Personne:
    """
    Représente une personne impliquée dans une affaire.
    """

    _role: str
    _nom: str
    identité: str
    adresse: str
    contact: str
    liens: str
    historique: str

    def __init__(
        self,
        role: str,
        nom: str,
        identité: str = "",
        adresse: str = "",
        contact: str = "",
        liens: str = "",
        historique: str = "",
    ):
        # On passe par les setters
        self.role = role
        self.nom = nom
        self.identité = identité
        self.adresse = adresse
        self.contact = contact
        self.liens = liens
        self.historique = historique

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, valeur: str) -> None:
        self._role = valeur or ""

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, valeur: str) -> None:
        self._nom = valeur or ""

    @classmethod
    def from_dict(cls, data: Dict) -> "Personne":
        return cls(
            role=data.get("role", ""),
            nom=data.get("nom", ""),
            identité=data.get("identité", ""),
            adresse=data.get("adresse", ""),
            contact=data.get("contact", ""),
            liens=data.get("liens", ""),
            historique=data.get("historique", ""),
        )

    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "nom": self.nom,
            "identité": self.identité,
            "adresse": self.adresse,
            "contact": self.contact,
            "liens": self.liens,
            "historique": self.historique,
        }
