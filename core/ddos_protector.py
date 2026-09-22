import time
import logging

logger = logging.getLogger("DDOS_PROTECTOR")

class DDoSProtector:
    """
    מנגנון הגנת קצב בקשות (Rate Limiting) ארגוני להגנה על נקודות הקצה הציבוריות 
    מפני התקפות הצפה (DDoS / Request Flooding).
    """
    def __init__(self, max_requests: int = 5, window_seconds: int = 1):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.client_history = {}  # ip -> list of timestamps

    def is_request_allowed(self, client_ip: str) -> bool:
        """בודק האם כתובת ה-IP הנוכחית חרגה ממכסת הבקשות המותרת בחלון הזמן"""
        current_time = time.time()
        
        if client_ip not in self.client_history:
            self.client_history[client_ip] = [current_time]
            return True

        # ניקוי חתימות זמן ישנות מחוץ לחלון המבוקש
        timestamps = [t for t in self.client_history[client_ip] if current_time - t <= self.window_seconds]
        self.client_history[client_ip] = timestamps

        if len(timestamps) >= self.max_requests:
            logger.warning(f"[!] Rate limit breached for IP: {client_ip} ({len(timestamps)} requests in window)")
            return False

        self.client_history[client_ip].append(current_time)
        return True
