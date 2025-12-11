import unittest
from core.models.personne import Personne


class TestPersonne(unittest.TestCase):

    def test_creation_personne(self):
        p = Personne(role="Victime", nom="John Doe")
        self.assertEqual(p.role, "Victime")
        self.assertEqual(p.nom, "John Doe")

    def test_to_dict(self):
        p = Personne(role="Témoin", nom="Alice", identité="ID123")
        d = p.to_dict()
        self.assertEqual(d["role"], "Témoin")
        self.assertEqual(d["nom"], "Alice")
        self.assertEqual(d["identité"], "ID123")

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
