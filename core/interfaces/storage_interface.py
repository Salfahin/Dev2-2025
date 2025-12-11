from __future__ import annotations
from typing import Protocol, Dict, Any, List


class StorageInterface(Protocol):
    """
    Interface définissant les opérations minimales qu'un système
    de stockage doit implémenter pour être utilisé par le projet.
    """

    def save(self, data: Dict[str, Any], filename: str) -> str:
        """
        Sauvegarde un dictionnaire dans un fichier identifié par filename.
        Retourne le chemin complet du fichier créé.
        """
        ...

    def load(self, filename: str) -> Dict[str, Any]:
        """
        Charge un fichier JSON et retourne un dictionnaire Python.
        """
        ...

    def delete(self, filename: str) -> None:
        """
        Supprime un fichier JSON du stockage.
        """
        ...

    def list_files(self) -> List[str]:
        """
        Retourne la liste des fichiers disponibles dans le stockage.
        """
        ...

    def load_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Charge tous les fichiers JSON du stockage sous forme :
        {
            "filename1.json": { ... },
            "filename2.json": { ... },
            ...
        }
        """
        ...
