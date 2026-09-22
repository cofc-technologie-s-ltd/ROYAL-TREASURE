# 👑 ROYAL-TREASURE Sovereign Enterprise Ecosystem (v2.9.3)

Welcome to **ROYAL-TREASURE**, a cutting-edge sovereign technology framework developed by **COFC Technologies LTD**. Designed for ultra-secure financial asset custody, multi-signature governance, and quantum-resistant network communication.

## 🚀 Key Architectural Highlights (v2.9.3)

* **Post-Quantum Cryptography (PQC):** Integrated NIST Level 5 lattice-based security (`PostQuantumGuardEngine` using CRYSTALS-Dilithium-V patterns) protecting all node communication and transactions against quantum compute threats.
* **M-of-N Multi-Sig Governance:** Cryptographically enforced Ed25519 multi-signature threshold verification (`AdminMultiSig`) for authorizing critical reserve releases.
* **Real-Time Oracle & P2P Sync:** Live gold price feeds via `OracleGateway` combined with resilient P2P node synchronization and exponential backoff retry mechanisms.
* **Sovereign Dashboard:** Web interface monitoring live node metrics, cryptographic keys, and asset valuations.

## 🛠️ Quick Deployment

Run the automated production deployment script:
```bash
chmod +x deploy_prod.sh
./deploy_prod.sh

🧪 Running Automated QA Tests
python -m unittest discover -s tests

Developed by COFC Technologies LTD (2026).
