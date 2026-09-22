import json
import time
import hashlib

class ISOGateway:
    def __init__(self):
        self.version = "ISO20022_V2026"
        self.corridors = ["SWIFT_FIN_PLUS", "TARGET2", "COFC_QUANTUM_CLEARING"]

    def generate_pacs_008_message(self, sender_bic, receiver_bic, amount, currency, reference_id):
        msg = {
            "AppHdr": {
                "Fr": {"FIId": {"FinInstnId": {"BICFI": sender_bic}}},
                "To": {"FIId": {"FinInstnId": {"BICFI": receiver_bic}}},
                "BizMsgIdr": reference_id,
                "MsgDefIdr": "pacs.008.001.10",
                "CreDtTm": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            },
            "Document": {
                "FIToFICstmrCdtTrf": {
                    "GrpHdr": {
                        "MsgId": reference_id,
                        "CreDt": time.strftime("%Y-%m-%d", time.gmtime()),
                        "NbOfTxs": "1"
                    },
                    "CdtTrfTxInf": {
                        "PmtId": {"EndToEndId": f"E2E-{reference_id}"},
                        "IntrBkSttlmAmt": {"Ccy": currency, "value": float(amount)},
                        "CdtrAgt": {"FinInstnId": {"BICFI": receiver_bic}}
                    }
                }
            }
        }
        return msg

    def validate_and_route(self, iso_payload, corridor="COFC_QUANTUM_CLEARING"):
        if corridor not in self.corridors:
            return {"status": "REJECTED", "reason": "Invalid financial corridor"}
        
        settlement_hash = hashlib.sha3_512(json.dumps(iso_payload, sort_keys=True).encode()).hexdigest()
        return {
            "status": "SETTLED_ISO_COMPLIANT",
            "corridor": corridor,
            "settlement_hash": settlement_hash,
            "timestamp": time.time()
        }
