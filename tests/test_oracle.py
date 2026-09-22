import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.oracle_gateway import OracleGateway

class TestOracleGateway(unittest.TestCase):
    
    def test_oracle_price_feed(self):
        oracle = OracleGateway(default_gold_price=2750.0)
        data = oracle.fetch_live_gold_price()
        
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["asset"], "GOLD")
        self.assertGreater(data["price_usd"], 0.0)
        self.assertIn("timestamp", data)

if __name__ == "__main__":
    unittest.main()
