# 👑 COFC TECHNOLOGIES LTD - ROYAL-TREASURE Hardware Vault Dockerfile (v3.3.0)
FROM python:3.13-slim

# הגדרת סביבת עבודה מנותקת ומאובטחת
WORKDIR /app

# התקנת תלויות מערכת נדרשות לצורך הצפנה קריפטוגרפית (PQC & Ed25519)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# העתקת מודולי הליבה וקוד בקר החומרה למכולה
COPY core/ /app/core/
COPY clients/ /app/clients/

# התקנת חבילות Python הנדרשות (כגון cryptography)
RUN pip install --no-cache-dir cryptography

# הגדרת משתני סביבה לאבטחת החומרה
ENV VAULT_MODE=AIR_GAPPED
ENV PQC_SECURITY_LEVEL=5
ENV ENVIRONMENT=PRODUCTION

# הפעלת בקר החומרה במצב מנותק
CMD ["python", "clients/hardware_vault.py"]

