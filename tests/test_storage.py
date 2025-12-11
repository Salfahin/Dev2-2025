import unittest
import tempfile
import os
from core.services.storage_service import StorageService


class TestStorageService(unittest.TestCase):

    def setUp(self):
        # Crée un dossier temporaire pour stocker les JSON de test
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageService(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load(self):
        data = {"titre": "Affaire A"}
        path = self.storage.save(data)

        filename = os.path.basename(path)
        loaded = self.storage.load(filename)

        self.assertEqual(loaded["titre"], "Affaire A")

    def test_list_files(self):
        self.storage.save({"a": 1})
        self.storage.save({"b": 2})
        files = self.storage.list_files()

        self.assertEqual(len(files), 2)

    def test_delete(self):
        path = self.storage.save({"x": 1})
        filename = os.path.basename(path)

        self.storage.delete(filename)

        self.assertEqual(self.storage.list_files(), [])

    def test_load_all(self):
        self.storage.save({"t": 1})
        self.storage.save({"t": 2})

        loaded = self.storage.load_all()
        self.assertEqual(len(loaded), 2)
