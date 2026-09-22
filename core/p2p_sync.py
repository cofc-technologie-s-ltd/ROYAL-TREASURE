import urllib.request
import json
import logging

logger = logging.getLogger("P2P_SYNC")

class P2PNodeSyncer:
    """
    מנהל סנכרון מצב מול צמתים עמיתים (Peer Nodes) ברשת המבוזרת של COFC.
    """
    def __init__(self, node_id: str, peer_endpoints: list = None):
        self.node_id = node_id
        self.peer_endpoints = peer_endpoints or []

    def broadcast_state(self, state_payload: dict):
        """משדר את מצב ה-Ledger או האורקל לצמתים השכנים ברשת"""
        data = json.dumps(state_payload).encode('utf-8')
        for peer in self.peer_endpoints:
            try:
                req = urllib.request.Request(
                    f"{peer}/api/p2p/sync",
                    data=data,
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=2) as response:
                    logger.info(f"[+] Successfully synced state with peer {peer}")
            except Exception as e:
                logger.warning(f"[-] Failed to sync with peer {peer}: {e}")
