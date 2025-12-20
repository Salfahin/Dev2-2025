from dataclasses import dataclass


class ArmeValidationError(Exception):
    """Erreur de validation d'une arme."""
@dataclass
class Arme:
    _type_arme: str | None = None
    _nom_arme: str | None = None
    _serie_id_arme: int | None = None

    @property
    def type_arme(self) -> str | None:
        return self._type_arme
    
    @type_arme.setter
    def type_arme(self, valeur: str |None) -> None:
        if valeur is not None and valeur.strip() == "":
            raise ArmeValidationError("Le type d'arme ne peut être vide.")
        self._type_arme = valeur
        self._validate()

    @property
    def nom_arme(self) -> str | None:
        return self._nom_arme

    @nom_arme.setter
    def nom_arme(self, valeur: str | None) -> None:
        if valeur is not None and valeur.strip() == "":
            raise ArmeValidationError("Le nom de l’arme ne peut pas être vide.")
        self._nom_arme = valeur
        self._validate()

    # -------------------
    # NUMÉRO DE SÉRIE
    # -------------------
    @property
    def serie_id_arme(self) -> int | None:
        return self._serie_id_arme

    @serie_id_arme.setter
    def serie_id_arme(self, valeur: int | None) -> None:
        if valeur is not None and valeur.strip() == "":
            raise ArmeValidationError("Le numéro de série ne peut pas être vide.")
        self._serie_id_arme = valeur
        self._validate()


    # -------------------
    # VALIDATION MÉTIER
    # -------------------
    def _validate(self) -> None:
        """
        Règle métier:
        - si type_arme est défini -> nom ET numéro de série obligatoires
        """
        if self._type_arme:
            if not self._nom_arme:
                raise ArmeValidationError(
                    "Le nom est obligatoire si un type d’arme est renseigné."
                )
            if not self._serie_id_arme:
                raise ArmeValidationError(
                    "Le numéro de série est obligatoire si un type d’arme est renseigné."
                )
            

    # -------------------
    # transformer en JSON
    # -------------------
    def to_dict(self) -> dict:
        return {
            "type_arme": self.type_arme,
            "nom_arme": self.nom_arme,
            "serie_id_arme": self.serie_id_arme,
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Arme":
        a = Arme()

        # IMPORTANT : d'abord nom + série puis type (validation)
        a.nom_arme = data.get("nom_arme")
        a.serie_id_arme = data.get("serie_id_arme")
        a.type_arme = data.get("type_arme")

        return a
