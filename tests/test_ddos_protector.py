import unittest
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.ddos_protector import DDoSProtector

class TestDDoSProtector(unittest.TestCase):
    
    def setUp(self):
        # אתחול הגנה קשיחה: מקסימום 2 בקשות בשנייה
        self.protector = DDoSProtector(max_requests=2, window_seconds=1)

    def test_request_allowed_flow(self):
        """ודאות אישור בקשות תחת המכסה המותרת"""
        self.assertTrue(self.protector.is_request_allowed("192.168.1.1"))
        self.assertTrue(self.protector.is_request_allowed("192.168.1.1"))

    def test_rate_limit_blocking(self):
        """ודאות חסימת בקשות חורגות (Rate Limiting Activation)"""
        self.assertTrue(self.protector.is_request_allowed("10.0.0.1"))
        self.assertTrue(self.protector.is_request_allowed("10.0.0.1"))
        # הבקשה השלישית ברצף צריכה להיחסם מיד
        self.assertFalse(self.protector.is_request_allowed("10.0.0.1"))

if __name__ == "__main__":
    unittest.main()
