from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from core.models.personne import Personne
from core.models.arme import Arme

@dataclass
class Affaire:
    """
    Représente une affaire complète, manipulée par la logique métier.
    """
    titre: str
    date: str
    lieu: str
    type_affaire: str

    description: str = ""
    armes: list[Arme] = field(default_factory=list)
    responsables: str = ""
    photos: List[str] = field(default_factory=list)
    personnes: List[Personne] = field(default_factory=list)

    etat: str = "🟢 En cours"
    urgence: str = "⚪ Faible"

    path: Optional[str] = None  # chemin du fichier JSON si existant

    # ---------------------------------------------------------
    #           CONVERSION DICT <-> OBJET MÉTIER
    # ---------------------------------------------------------
    @staticmethod
    def from_dict(data: Dict, path: Optional[str] = None) -> "Affaire":
        """
        Construit une Affaire à partir d'un dictionnaire chargé depuis JSON.
        """
        personnes = [
            Personne.from_dict(p) for p in data.get("personnes", [])
        ]


        return Affaire(
            titre=data.get("titre", ""),
            date=data.get("date", ""),
            lieu=data.get("lieu", ""),
            type_affaire=data.get("type_affaire", ""),
            description=data.get("description", ""),
            responsables=data.get("responsables", ""),
            armes = [Arme.from_dict(a) for a in (data.get("armes", []) or [])],
            photos=data.get("photos", []),
            personnes=personnes,
            etat=data.get("etat", "🟢 En cours"),
            urgence=data.get("urgence", "⚪ Faible"),
            path=path
            
        )

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
            "armes": [a.to_dict() for a in (self.armes or [])],
            "photos": self.photos,
            "etat": self.etat,
            "urgence": self.urgence,
            "personnes": [p.to_dict() for p in self.personnes]
            
        }

    # ---------------------------------------------------------
    #        MÉTHODES UTILITAIRES (compteurs, etc.)
    # ---------------------------------------------------------
    def nombre_victimes(self) -> int:
        return sum(1 for p in self.personnes if "Victime" in p.role)

    def nombre_suspects(self) -> int:
        return sum(1 for p in self.personnes if "Suspect" in p.role)

    def nombre_temoins(self) -> int:
        return sum(1 for p in self.personnes if "témo" in p.role.lower())
