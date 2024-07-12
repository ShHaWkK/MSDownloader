import unittest
import os
from src.converter import Converter

class TestConverter(unittest.TestCase):
    def setUp(self):
        self.converter = Converter()
        self.test_input = "test_input.mp4"
        self.test_output = "test_output.mp4"

    def test_convert_to_mp4(self):
        # Assurez-vous d'avoir un fichier test_input.mp4 dans le même dossier
        result = self.converter.convert_to_mp4(self.test_input, self.test_output)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_output))

    def tearDown(self):
        if os.path.exists(self.test_output):
            os.remove(self.test_output)

if __name__ == '__main__':
    unittest.main()
