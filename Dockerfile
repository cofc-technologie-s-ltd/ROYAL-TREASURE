# استخدام Python 3.13 הרשמי כבסיס לקונטיינר
FROM python:3.13-slim

# הגדרת תיקיית העבודה בתוך הקונטיינר
WORKDIR /app

# התקנת תלויות מערכת בסיסיות (כגון כלי רשת או ניקוי מטמון)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# העתקת קבצי הקוד והפרויקט לתוך הקונטיינר
COPY core/ ./core/
COPY server/ ./server/
COPY tests/ ./tests/
COPY ledger_db.sqlite* ./ 

# הגדרת משתני סביבה למצב ייצור
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=PRODUCTION

# חשיפת הפורט של שרת ה-Enterprise Sovereign Node
EXPOSE 8080

# פקודת ההפעלה הראשית של הקונטיינר (הרצת השרת והבדיקות במידת הצורך)
CMD ["python", "server/enterprise_node.py"]
