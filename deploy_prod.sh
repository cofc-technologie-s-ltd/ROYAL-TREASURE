#!/bin/bash
echo "====================================================================="
echo "🚀 COFC TECHNOLOGIES LTD - DEPLOYING DISTRIBUTED MESH NETWORK v3.1.5"
echo "====================================================================="

# יצירת תיקיית הנתונים עבור נפחי הדיסק המופרדים
mkdir -p data

echo "[*] Tearing down legacy isolated nodes..."
docker compose down --remove-orphans 2>/dev/null

echo "[*] Building and orchestrating multi-node sovereign mesh..."
docker compose up --build -d

echo "[*] Waiting for network topology initialization..."
sleep 4

# בדיקת בריאות לצומת אלפא
if curl -s http://127.0.0 > /dev/null; then
    echo "🟢 SUCCESS: Node Alpha operational on port 8080"
else
    echo "🔴 ERROR: Node Alpha failed to launch."
    exit 1
fi

# בדיקת בריאות לצומת בטא
if curl -s http://127.0.0 > /dev/null; then
    echo "🟢 SUCCESS: Node Beta operational on port 8081"
else
    echo "🔴 ERROR: Node Beta failed to launch."
    exit 1
fi

echo "====================================================================="
echo "💎 COFC MULTI-NODE NETWORKING IS LIVE & DISCOVERABLE!"
echo "📊 Node Alpha Dashboard: http://127.0.0"
echo "📊 Node Beta Dashboard:  http://127.0.0"
echo "====================================================================="
