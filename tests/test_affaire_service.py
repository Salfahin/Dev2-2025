import unittest
from unittest.mock import MagicMock

from core.services.affaire_service import AffaireService
from core.models.affaire import Affaire


class TestAffaireService(unittest.TestCase):

    def setUp(self):
        # Fake storage pour mocker les opérations
        self.storage = MagicMock()
        self.service = AffaireService(self.storage)

    def test_get_all(self):
        self.storage.load_all.return_value = {
            "file1.json": {"titre": "A", "date": "2024", "lieu": "Paris", "type_affaire": "Vol"},
            "file2.json": {"titre": "B", "date": "2024", "lieu": "Lyon", "type_affaire": "Fraude"},
        }
        affaires = self.service.get_all()

        self.assertEqual(len(affaires), 2)
        self.assertEqual(affaires[0].titre, "A")

    def test_trier_par_etat(self):
        a1 = Affaire("A", "2024", "Paris", "Vol", etat="🟢 En cours")
        a2 = Affaire("B", "2024", "Paris", "Vol", etat="🟡 À surveiller")
        a3 = Affaire("C", "2024", "Paris", "Vol", etat="🔵 Gelée — manque d'informations")

        en_cours, surveiller, gelee = self.service.trier_par_etat([a1, a2, a3])

        self.assertEqual(len(en_cours), 1)
        self.assertEqual(len(surveiller), 1)
        self.assertEqual(len(gelee), 1)

    def test_affaires_classees(self):
        a1 = Affaire("A", "2024", "Paris", "Vol", etat="🟣 Affaire classée")
        a2 = Affaire("B", "2024", "Paris", "Vol", etat="🟢 En cours")

        result = self.service.affaires_classees([a1, a2])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].titre, "A")

    def test_save(self):
        a = Affaire("A", "2024", "Paris", "Vol")
        self.service.save(a)

        self.assertTrue(self.storage.save.called)
