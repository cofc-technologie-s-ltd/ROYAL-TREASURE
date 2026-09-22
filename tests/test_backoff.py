import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.backoff import exponential_backoff_retry

class TestExponentialBackoff(unittest.TestCase):
    
    def test_successful_execution_on_first_try(self):
        """ בדיקה שהפונקציה רצה בהצלחה בניסיון הראשון ללא השהיה מיותרת """
        call_count = 0

        @exponential_backoff_retry(max_retries=3, base_delay=0.1)
        def non_failing_func():
            nonlocal call_count
            call_count += 1
            return "SUCCESS"

        result = non_failing_func()
        self.assertEqual(result, "SUCCESS")
        self.assertEqual(call_count, 1)

    def test_recovery_after_temporary_failures(self):
        """ בדיקה שהמנגנון מתאושש בהצלחה לאחר מספר כישלונות זמניים """
        attempt_count = 0

        @exponential_backoff_retry(max_retries=3, base_delay=0.05)
        def flaky_func():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ConnectionError("Simulated Network Drop")
            return "RECOVERED"

        result = flaky_func()
        self.assertEqual(result, "RECOVERED")
        self.assertEqual(attempt_count, 3)

    def test_max_retries_exhaustion(self):
        """ בדיקה שכאשר עוברים את מקסימום הניסיונות, נזרקת שגיאה כמצופה """
        @exponential_backoff_retry(max_retries=2, base_delay=0.01)
        def always_fail_func():
            raise TimeoutError("Server Unreachable")

        with self.assertRaises(TimeoutError):
            always_fail_func()

if __name__ == "__main__":
    unittest.main()
