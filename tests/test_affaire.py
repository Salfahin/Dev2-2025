import unittest
from core.models.affaire import Affaire
from core.models.personne import Personne


class TestAffaire(unittest.TestCase):

    def test_creation_affaire(self):
        a = Affaire(
            titre="Test",
            date="2024",
            lieu="Paris",
            type_affaire="Vol"
        )
        self.assertEqual(a.titre, "Test")
        self.assertEqual(a.lieu, "Paris")

    def test_personnes_compteurs(self):
        a = Affaire(
            titre="A",
            date="2024",
            lieu="Paris",
            type_affaire="Vol",
            personnes=[
                Personne(role="Victime", nom="A"),
                Personne(role="Suspect", nom="B"),
                Personne(role="Témoin", nom="C"),
                Personne(role="Victime", nom="D")
            ]
        )
        self.assertEqual(a.nombre_victimes(), 2)
        self.assertEqual(a.nombre_suspects(), 1)
        self.assertEqual(a.nombre_temoins(), 1)

    def test_to_dict_and_back(self):
        a = Affaire(
            titre="Test",
            date="2024",
            lieu="Paris",
            type_affaire="Vol",
            description="Desc",
            urgence="🟠 Élevé",
            personnes=[
                Personne(role="Victime", nom="John")
            ]
        )
        data = a.to_dict()
        a2 = Affaire.from_dict(data)

        self.assertEqual(a2.titre, "Test")
        self.assertEqual(len(a2.personnes), 1)
        self.assertEqual(a2.urgence, "🟠 Élevé")
