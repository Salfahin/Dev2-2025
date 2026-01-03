import unittest
from core.models.affaire import Affaire
from core.models.personne import Personne


class TestAffaire(unittest.TestCase):

    def test_creation_affaire_pre_post(self):
        # --------------------
        # PRÉCONDITIONS
        # --------------------
        titre = "Test"
        lieu = "Paris"

        # --------------------
        # ACTION
        # --------------------
        a = Affaire(
            titre=titre,
            date="2024",
            lieu=lieu,
            type_affaire="Vol"
        )

        # --------------------
        # POSTCONDITIONS
        # --------------------
        self.assertEqual(a.titre, titre)
        self.assertEqual(a.lieu, lieu)
        self.assertEqual(a.type_affaire, "Vol")

    def test_personnes_compteurs_pre_post(self):
        # --------------------
        # PRÉCONDITIONS
        # --------------------
        personnes = [
            Personne(role="Victime", nom="A"),
            Personne(role="Suspect", nom="B"),
            Personne(role="Témoin", nom="C"),
            Personne(role="Victime", nom="D")
        ]

        a = Affaire(
            titre="A",
            date="2024",
            lieu="Paris",
            type_affaire="Vol",
            personnes=personnes
        )

        # Vérification des préconditions
        self.assertEqual(len(a.personnes), 4)

        # --------------------
        # ACTION
        # --------------------
        nb_victimes = a.nombre_victimes()
        nb_suspects = a.nombre_suspects()
        nb_temoins = a.nombre_temoins()

        # --------------------
        # POSTCONDITIONS
        # --------------------
        self.assertEqual(nb_victimes, 2)
        self.assertEqual(nb_suspects, 1)
        self.assertEqual(nb_temoins, 1)
