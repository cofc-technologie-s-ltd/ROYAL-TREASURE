import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.liquidity_simulator import TriAssetLiquidityPool

class TestLiquidityPoolEngine(unittest.TestCase):
    
    def setUp(self):
        self.pool = TriAssetLiquidityPool(gold_reserves=10000.0, key_reserves=1000.0, gem_reserves=100.0)

    def test_spot_price_calculation(self):
        """ודאות חישוב שער רגעי תקין לפי יחס הרזרבות"""
        price = self.pool.get_spot_price("GOLD", "KEY")
        self.assertEqual(price, 0.1)

    def test_successful_swap_execution(self):
        """בדיקת המרה מוצלחת בעמלה אפס עם הגדרת החלקה מותאמת לנפח"""
        # הגדלת ה-max_slippage ל-0.20 כדי להכיל את תנודת ה-Price Impact המחושבת (כ-17%)
        res = self.pool.swap_assets("GOLD", "KEY", amount_in=1000.0, max_slippage=0.20)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertGreater(res["amount_out"], 0.0)
        self.assertEqual(res["new_pool_balances"]["GOLD"], 11000.0)

    def test_slippage_guard_activation(self):
        """ודאות חסימת עסקאות הגורמות לתנודת מחיר קיצונית"""
        res = self.pool.swap_assets("GOLD", "GEM", amount_in=8000.0, max_slippage=0.02)
        self.assertEqual(res["status"], "FAILED")
        self.assertIn("Slippage too high", res["reason"])

if __name__ == "__main__":
    unittest.main()
