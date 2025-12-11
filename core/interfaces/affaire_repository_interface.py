from __future__ import annotations
from typing import Protocol, List
from core.models.affaire import Affaire


class AffaireRepositoryInterface(Protocol):
    """
    Interface définissant les opérations métier disponibles pour manipuler les affaires.
    """

    def get_all(self) -> List[Affaire]:
        """
        Retourne toutes les affaires chargées depuis le stockage.
        """
        ...

    def get_by_path(self, path: str) -> Affaire:
        """
        Charge une affaire spécifique depuis son fichier JSON.
        """
        ...

    def save(self, affaire: Affaire) -> str:
        """
        Sauvegarde une affaire en JSON (création ou mise à jour).
        Retourne le chemin complet du fichier.
        """
        ...

    def delete(self, affaire: Affaire) -> None:
        """
        Supprime le fichier JSON associé à l'affaire.
        """
        ...
