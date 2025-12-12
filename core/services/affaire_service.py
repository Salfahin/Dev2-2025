from __future__ import annotations

from typing import List, Dict
from core.models.affaire import Affaire
from core.interfaces.affaire_repository_interface import AffaireRepositoryInterface
from core.interfaces.storage_interface import StorageInterface


class AffaireService(AffaireRepositoryInterface):
    """
    Service métier principal qui manipule les objets 'Affaire' :
    chargement, sauvegarde, filtrage, suppression, tri, etc.
    """

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    # -----------------------------------------------------------
    #   CHARGER TOUTES LES AFFAIRES
    # -----------------------------------------------------------
    def get_all(self) -> List[Affaire]:
        raw_data = self.storage.load_all()
        affaires = []

        for filename, data in raw_data.items():
            path = filename  # identifiant interne
            affaire = Affaire.from_dict(data, path=path)
            affaires.append(affaire)

        return affaires

    # -----------------------------------------------------------
    #   CHARGER UNE AFFAIRE SPÉCIFIQUE
    # -----------------------------------------------------------
    def get_by_path(self, path: str) -> Affaire:
        data = self.storage.load(path)
        return Affaire.from_dict(data, path=path)

    # -----------------------------------------------------------
    #   SAUVEGARDER UNE AFFAIRE
    # -----------------------------------------------------------
    def save(self, affaire: Affaire) -> str:
        data = affaire.to_dict()

        filename = affaire.path if affaire.path else None

        saved_path = self.storage.save(data, filename)
        affaire.path = saved_path.split("/")[-1]  # identifiant interne
        return saved_path

    # -----------------------------------------------------------
    #   SUPPRIMER UNE AFFAIRE
    # -----------------------------------------------------------
    def delete(self, affaire: Affaire) -> None:
        if affaire.path:
            self.storage.delete(affaire.path)

    # -----------------------------------------------------------
    #   MÉTHODES DE TRI / FILTRAGE
    # -----------------------------------------------------------
    def trier_par_etat(self, affaires: List[Affaire]):
        en_cours = [a for a in affaires if "En cours" in a.etat]
        surveiller = [a for a in affaires if "surveiller" in a.etat.lower()]
        gelee = [a for a in affaires if "gel" in a.etat.lower()]
        return en_cours, surveiller, gelee

    def affaires_classees(self, affaires: List[Affaire]):
        return [a for a in affaires if "class" in a.etat.lower()]
