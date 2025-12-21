import unittest
from datetime import datetime
from gui.filtre_v2 import Affaire, ListeAffaires, rafraichir_tri

class TestAffaire(unittest.TestCase):

    def setUp(self):
        self.data = {
            "titre": "Affaire Test",
            "date_dernier_mouvement": datetime(2025, 12, 21),
            "lieu": "Paris",
            "responsable": "Alice",
            "urgence": 5
        }
        self.affaire = Affaire(self.data)

    def test_proprietes(self):
        self.assertEqual(self.affaire.titre, "affaire test")
        self.assertEqual(self.affaire.date_dernier_mouvement, self.data["date_dernier_mouvement"])
        self.assertEqual(self.affaire.lieu, "paris")
        self.assertEqual(self.affaire.responsable, "alice")
        self.assertEqual(self.affaire.urgence, 5)

    def test_proprietes_manquantes(self):
        a = Affaire({})
        self.assertEqual(a.titre, "")
        self.assertIsNone(a.date_dernier_mouvement)
        self.assertEqual(a.lieu, "")
        self.assertEqual(a.responsable, "")
        self.assertEqual(a.urgence, 0)


class TestListeAffaires(unittest.TestCase):

    def setUp(self):
        self.affaires_data = [
            {"titre": "B", "date_dernier_mouvement": datetime(2025, 12, 20), "lieu": "Lyon", "responsable": "Bob", "urgence": 3},
            {"titre": "A", "date_dernier_mouvement": datetime(2025, 12, 21), "lieu": "Paris", "responsable": "Alice", "urgence": 5},
            {"titre": "C", "date_dernier_mouvement": datetime(2025, 12, 19), "lieu": "Marseille", "responsable": "Charlie", "urgence": 1},
        ]
        self.liste = ListeAffaires(self.affaires_data)

    def test_tri_ordre_alphabetique(self):
        result = self.liste.trier("ordre alphabétique")
        titres = [a.titre for a in result]
        self.assertEqual(titres, ["a", "b", "c"])

    def test_tri_date(self):
        result = self.liste.trier("date")
        dates = [a.date_dernier_mouvement for a in result]
        self.assertEqual(dates, [
            datetime(2025, 12, 19),
            datetime(2025, 12, 20),
            datetime(2025, 12, 21)
        ])

    def test_tri_lieu(self):
        result = self.liste.trier("lieu")
        lieux = [a.lieu for a in result]
        self.assertEqual(lieux, ["lyon", "marseille", "paris"])

    def test_tri_responsable(self):
        result = self.liste.trier("responsable")
        responsables = [a.responsable for a in result]
        self.assertEqual(responsables, ["alice", "bob", "charlie"])

    def test_tri_urgence(self):
        result = self.liste.trier("urgence")
        urgences = [a.urgence for a in result]
        self.assertEqual(urgences, [5, 3, 1])

    def test_tri_invalide(self):
        # Doit retourner la liste originale si critère invalide
        result = self.liste.trier("invalide")
        titres = [a.titre for a in result]
        self.assertEqual(titres, ["b", "a", "c"])


if __name__ == "__main__":
    unittest.main()
