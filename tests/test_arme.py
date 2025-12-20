import unittest
from core.models.arme import Arme, ArmeValidationError

class TestArme(unittest.TestCase):
    """
    Si le type d'arme est fourni num de série et nom d'arme doivent être rempli
    Les 2 premiers méthodes testent une premier fois sans nom et la 2e sans num de série
    La 3e test tout
    """
    def test_type_sans_nom_declenche_exception(self):
        a = Arme()
        a.serie_id_arme = "12345"  # série OK, nom manquant

        with self.assertRaises(ArmeValidationError):
            a.type_arme = "Pistolet"  # doit lever l'exception
            
    def test_type_sans_serie_declenche_exception(self):
        a = Arme()
        a.nom_arme = "Glock 19"  # nom AOK, série manquante

        with self.assertRaises(ArmeValidationError):
            a.type_arme = "Pistolet"  # doit lever l'exception

    def test_arme_valide_ne_declenche_pas_exception(self):
        a = Arme()
        a.nom_arme = "Glock 19"
        a.serie_id_arme = "12345"
        a.type_arme = "Pistolet"  # ordre important

        self.assertEqual(a.type_arme, "Pistolet")

if __name__ == "__main__":
    unittest.main()
