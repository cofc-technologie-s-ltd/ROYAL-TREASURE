#!/bin/bash
set -e

echo "[+] Starting ROYAL-TREASURE Enterprise Production Deployment (v2.9.3)..."

# 1. ניקוי קונטיינרים ישנים
echo "[+] Cleaning up legacy Docker containers..."
docker ps -a --filter "name=royal-treasure-node" -q | xargs -r docker rm -f || true

# 2. בניית תמונת ה-Docker
echo "[+] Building production Docker image for ROYAL-TREASURE node..."
docker build -t royal-treasure:v2.9.3 .

# 3. הרצת הקונטיינר בפורט 8080
echo "[+] Launching sovereign node container on port 8080..."
docker run -d --name royal-treasure-node -p 8080:8080 royal-treasure:v2.9.3

# 4. בדיקת בריאות אוטומטית (Health Check)
echo "[+] Performing automated health check on http://localhost:8080/api/metrics..."
sleep 3

HEALTH_CHECK=$(curl -s http://localhost:8080/api/metrics | grep -o "ONLINE" || true)

if [ "$HEALTH_CHECK" = "ONLINE" ]; then
    echo "[SUCCESS] ROYAL-TREASURE node v2.9.3 is ONLINE and fully healthy!"
else
    echo "[ERROR] Health check failed. Inspect container logs with 'docker logs royal-treasure-node'."
    exit 1
fi
