import unittest
from core.models.personne import Personne


class TestPersonne(unittest.TestCase):

    def test_creation_personne(self):
        p = Personne(role="Victime", nom="John Doe")
        self.assertEqual(p.role, "Victime")
        self.assertEqual(p.nom, "John Doe")
        self.assertEqual(p.identité, "")
        self.assertEqual(p.adresse, "")
        self.assertEqual(p.contact, "")
        self.assertEqual(p.liens, "")
        self.assertEqual(p.historique, "")

    def test_to_dict(self):
        p = Personne(
            role="Témoin",
            nom="Alice",
            identité="ID123",
            adresse="Rue X",
            contact="000",
            liens="Collègue",
            historique="RAS"
        )
        d = p.to_dict()
        self.assertEqual(d["role"], "Témoin")
        self.assertEqual(d["nom"], "Alice")
        self.assertEqual(d["identité"], "ID123")
        self.assertEqual(d["adresse"], "Rue X")
        self.assertEqual(d["contact"], "000")
        self.assertEqual(d["liens"], "Collègue")
        self.assertEqual(d["historique"], "RAS")

    def test_from_dict(self):
        data = {
            "role": "Suspect",
            "nom": "Bob",
            "adresse": "Rue A",
            "contact": "0000"
        }
        p = Personne.from_dict(data)
        self.assertEqual(p.role, "Suspect")
        self.assertEqual(p.nom, "Bob")
        self.assertEqual(p.adresse, "Rue A")
        self.assertEqual(p.contact, "0000")
        self.assertEqual(p.identité, "")
        self.assertEqual(p.liens, "")
        self.assertEqual(p.historique, "")

    def test_round_trip_dict(self):
        p1 = Personne(role="Expert", nom="Dr X", historique="Analyse ADN")
        p2 = Personne.from_dict(p1.to_dict())
        self.assertEqual(p1, p2)
