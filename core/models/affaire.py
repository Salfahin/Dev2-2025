from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from core.models.personne import Personne


@dataclass
class Affaire:
    """
    Représente une affaire complète, manipulée par la logique métier.
    """

    # ---------------------------------------------------------
    #   ATTRIBUTS PRINCIPAUX
    # ---------------------------------------------------------
    titre: str
    date: str
    lieu: str
    type_affaire: str

    description: str = ""
    responsables: str = ""
    photos: List[str] = field(default_factory=list)
    personnes: List[Personne] = field(default_factory=list)

    # Attributs internes protégés (utilisés par les setters)
    _etat: str = "🟢 En cours"
    _urgence: str = "⚪ Faible"

    path: Optional[str] = None  # chemin du fichier JSON si existant

    # ---------------------------------------------------------
    #   GETTERS / SETTERS (GUETTEURS)
    # ---------------------------------------------------------
    @property
    def etat(self) -> str:
        return self._etat

    @etat.setter
    def etat(self, valeur: str) -> None:
        etats_autorises = {
            "🟢 En cours",
            "🟡 À surveiller",
            "🔵 Gelée — manque d'informations",
        }
        if valeur not in etats_autorises:
            raise ValueError(f"État invalide : {valeur}")
        self._etat = valeur

    @property
    def urgence(self) -> str:
        return self._urgence

    @urgence.setter
    def urgence(self, valeur: str) -> None:
        urgences_autorisees = {
            "⚪ Faible",
            "🟡 Moyen",
            "🟠 Élevé",
            "🔴 Critique",
        }
        if valeur not in urgences_autorisees:
            raise ValueError(f"Urgence invalide : {valeur}")
        self._urgence = valeur

    # ---------------------------------------------------------
    #   INITIALISATION POST-CONSTRUCTEUR
    # ---------------------------------------------------------
    def __post_init__(self):
        """
        Garantit que les valeurs initiales passent par les setters
        même lors de la construction via la dataclass.
        """
        self.etat = self._etat
        self.urgence = self._urgence

    # ---------------------------------------------------------
    #   CONVERSION DICT <-> OBJET MÉTIER
    # ---------------------------------------------------------
    @staticmethod
    def from_dict(data: Dict, path: Optional[str] = None) -> "Affaire":
        """
        Construit une Affaire à partir d'un dictionnaire chargé depuis JSON.
        """
        personnes = [
            Personne.from_dict(p) for p in data.get("personnes", [])
        ]

        affaire = Affaire(
            titre=data.get("titre", ""),
            date=data.get("date", ""),
            lieu=data.get("lieu", ""),
            type_affaire=data.get("type_affaire", ""),
            description=data.get("description", ""),
            responsables=data.get("responsables", ""),
            photos=data.get("photos", []),
            personnes=personnes,
            path=path
        )

        # Passage volontaire par les setters
        affaire.etat = data.get("etat", "🟢 En cours")
        affaire.urgence = data.get("urgence", "⚪ Faible")

        return affaire

    def to_dict(self) -> Dict:
        """
        Convertit l'affaire en dictionnaire prêt à être sauvegardé en JSON.
        """
        return {
            "titre": self.titre,
            "date": self.date,
            "lieu": self.lieu,
            "type_affaire": self.type_affaire,
            "description": self.description,
            "responsables": self.responsables,
            "photos": self.photos,
            "etat": self.etat,
            "urgence": self.urgence,
            "personnes": [p.to_dict() for p in self.personnes]
        }

    # ---------------------------------------------------------
    #   MÉTHODES UTILITAIRES (COMPTEURS)
    # ---------------------------------------------------------
    def nombre_victimes(self) -> int:
        return sum(1 for p in self.personnes if "Victime" in p.role)

    def nombre_suspects(self) -> int:
        return sum(1 for p in self.personnes if "Suspect" in p.role)

    def nombre_temoins(self) -> int:
        return sum(1 for p in self.personnes if "témoin" in p.role.lower())
