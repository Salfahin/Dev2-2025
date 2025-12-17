import unittest
import tempfile
import os
from core.services.storage_service import StorageService


class TestStorageService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageService(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load(self):
        data = {"titre": "Affaire A"}
        path = self.storage.save(data)

        self.assertTrue(os.path.exists(path))

        filename = os.path.basename(path)
        loaded = self.storage.load(filename)

        self.assertEqual(loaded["titre"], "Affaire A")

    def test_list_files(self):
        self.storage.save({"a": 1})
        self.storage.save({"b": 2})

        files = self.storage.list_files()
        self.assertIsInstance(files, list)
        self.assertEqual(len(files), 2)

    def test_delete(self):
        path = self.storage.save({"x": 1})
        filename = os.path.basename(path)

        self.storage.delete(filename)

        self.assertEqual(len(self.storage.list_files()), 0)

    def test_load_all(self):
        self.storage.save({"t": 1})
        self.storage.save({"t": 2})

        loaded = self.storage.load_all()

        self.assertIsInstance(loaded, dict)
        self.assertEqual(len(loaded), 2)

        for filename, content in loaded.items():
            self.assertTrue(filename.endswith(".json"))
            self.assertIn("t", content)
