import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from clients.sovereign_wallet import SovereignWalletClient

class TestSovereignWalletClient(unittest.TestCase):
    
    def setUp(self):
        # בדיקת אינטגרציה מקומית מול מבנה הלקוח
        self.client = SovereignWalletClient(node_url="http://127.0.0.1:8080")

    def test_client_initialization(self):
        """ודאות אתחול הגדרות השרת בלקוח הנייד"""
        self.assertEqual(self.client.node_url, "http://127.0.0.1:8080")

if __name__ == "__main__":
    unittest.main()
