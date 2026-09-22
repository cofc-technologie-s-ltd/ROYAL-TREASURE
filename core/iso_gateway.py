import json
import uuid
from datetime import datetime

class ISO20022SovereignGateway:
    def __init__(self):
        pass

    def generate_pacs008_settlement(self, sender, recipient, asset_type, amount):
        """מייצר הודעת סליקה מוסדית בתקן ISO 20022 (pacs.008.001.08) המותאמת לנכסי RPoS."""
        msg_id = f"COFC-ISO-{uuid.uuid4().hex[:12].upper()}"
        settlement_data = {
            "AppHdr": {
                "Fr": {"FIId": {"FinInstnId": {"BICFI": "COFCSVL1XXX"}}},
                "To": {"FIId": {"FinInstnId": {"BICFI": "SOVRTREASXXX"}}},
                "BizMsgIdr": msg_id,
                "MsgDefIdr": "pacs.008.001.08",
                "CreDtTm": datetime.utcnow().isoformat()
            },
            "Document": {
                "FIToFICstmrCdtTrf": {
                    "GrpHdr": {
                        "MsgId": msg_id,
                        "CreDtTm": datetime.utcnow().isoformat(),
                        "NbOfTxs": "1",
                        "SttlmInf": {
                            "SttlmMtd": "CLRG",
                            "ClrSys": {"Prtry": "ROYAL_RPoS_SHA3"}
                        }
                    },
                    "CdtTrfTxInf": {
                        "PmtId": {"EndToEndId": f"E2E-{msg_id}"},
                        "IntrBkSttlmAmt": {
                            "Ccy": asset_type,
                            "Amt": f"{amount:.4f}"
                        },
                        "Dbtr": {"Nm": sender},
                        "Cdtr": {"Nm": recipient},
                        "Purp": {"Prtry": "SOVEREIGN_ASSET_SETTLEMENT"}
                    }
                }
            }
        }
        return settlement_data
