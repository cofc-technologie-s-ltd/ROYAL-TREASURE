import time
import random
import logging

logger = logging.getLogger("BACKOFF_ENGINE")

def exponential_backoff_retry(max_retries=3, base_delay=1.0, max_delay=10.0):
    """
    דקורטור לביצוע ניסיונות חוזרים (Retries) עם השהיה מעריכית ו-Jitter 
    להתאוששות אוטונומית של מנוע הכרייה ותקשורת הצמתים.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            delay = base_delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"[-] Max retries ({max_retries}) reached for '{func.__name__}'. Error: {e}")
                        raise e
                    
                    # חישוב השהיה מעריכית עם הוספת רעש אקראי (Jitter) למניעת התנגשויות
                    jitter = random.uniform(0, 0.3)
                    sleep_time = min(delay + jitter, max_delay)
                    logger.warning(f"[!] Operation '{func.__name__}' failed ({e}). Retrying in {sleep_time:.2f}s (Attempt {retries}/{max_retries})...")
                    time.sleep(sleep_time)
                    delay *= 2
        return wrapper
    return decorator
