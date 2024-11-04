# tests/test_api_client.py
import unittest
from pyepisuite.api_client import EpiSuiteAPIClient
from pyepisuite.models import Identifiers

class TestEpiSuiteAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = EpiSuiteAPIClient()

    def test_search(self):
        identifiers = self.client.search('formaldehyde')
        self.assertIsInstance(identifiers, list)
        self.assertGreater(len(identifiers), 0)
        self.assertIsInstance(identifiers[0], Identifiers)
        self.assertEqual(identifiers[0].name, 'FORMALDEHYDE')

if __name__ == '__main__':
    unittest.main()