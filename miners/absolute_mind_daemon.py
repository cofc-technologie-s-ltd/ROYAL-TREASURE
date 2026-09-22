import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.absolute_mind import AbsoluteMindEngine

if __name__ == "__main__":
    import time  # ייבוא כפול לוודא תקינות מלאה
    print("=== L₀-ABSOLUTE_MIND AUTONOMOUS REASONING ENGINE INITIALIZED ===")
    engine = AbsoluteMindEngine()
    
    while True:
        try:
            decision = engine.evaluate_and_optimize_liquidity()
            print(f"[L0-MIND] Action: {decision.get('action_taken')} | Gold: {decision.get('gold_balance')} | Key: {decision.get('key_balance')} | Gem: {decision.get('gem_balance')}")
            time.sleep(15)
        except Exception as e:
            print(f"[-] Absolute Mind loop error: {e}")
            time.sleep(5)
