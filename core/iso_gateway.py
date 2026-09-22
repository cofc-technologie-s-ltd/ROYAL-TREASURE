import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

class ISOGateway:
    def __init__(self):
        self.gateway_status = "ISO_20022_ACTIVE"

    def validate_and_route(self, xml_message: str) -> dict:
        """
        מבצע אימות מבני וערכי קשיח (Structural Validation) להודעות pacs.008.
        מוודא תקינות קודי BIC, קודי מטבע ISO 4217, ופורמט המזהים הפיננסיים.
        """
        try:
            root = ET.fromstring(xml_message)
            
            # שימוש בתווים כלליים {*}, כדי להתעלם ממרחבי שמות (Namespaces) בעת החיפוש ב-XML
            bic_pattern = re.compile(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$")
            
            dbtr_agent = root.find(".//{*}DbtrAgt/{*}FinInstnId/{*}BICFI")
            cdtr_agent = root.find(".//{*}CdtrAgt/{*}FinInstnId/{*}BICFI")
            
            if dbtr_agent is None or not dbtr_agent.text or not bic_pattern.match(dbtr_agent.text):
                return {"status": "REJECTED", "reason": f"Invalid or missing Debtor Bank BIC: {dbtr_agent.text if dbtr_agent is not None else 'None'}"}
                
            if cdtr_agent is None or not cdtr_agent.text or not bic_pattern.match(cdtr_agent.text):
                return {"status": "REJECTED", "reason": f"Invalid or missing Creditor Bank BIC: {cdtr_agent.text if cdtr_agent is not None else 'None'}"}

            # 2. אימות קוד מטבע (חייב להיות 3 תווים לפי ISO 4217)
            amt_node = root.find(".//{*}IntrBkSttlmAmt")
            if amt_node is not None:
                currency = amt_node.get("Ccy")
                if not currency or not re.match(r"^[A-Z]{3}$", currency):
                    return {"status": "REJECTED", "reason": "Invalid Currency Code Format (ISO 4217 violation)"}
                
                try:
                    amount = float(amt_node.text)
                    if amount <= 0:
                        return {"status": "REJECTED", "reason": "Settlement amount must be greater than zero"}
                except ValueError:
                    return {"status": "REJECTED", "reason": "Malformed non-numeric settlement amount"}
            else:
                return {"status": "REJECTED", "reason": "Missing Interbank Settlement Amount node"}

            return {
                "status": "SETTLED",
                "iso_compliance": "COMPLIANT_PASS",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "routed_gateway": "COFC_ENTERPRISE_ROUTER"
            }

        except ET.ParseError:
            return {"status": "REJECTED", "reason": "Invalid XML structure: Failed to parse structural tags"}

    def generate_pacs_008_message(self, sender_bic: str, recv_bic: str, amount: float, currency: str, ref_id: str) -> str:
        """ מחולל הודעת XML תקנית של pacs.008 לצורך התחשבנות בנקאית """
        timestamp = datetime.now(timezone.utc).isoformat()
        return f"""<?xml version="1.0" encoding="utf-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">
    <FIToFICstmrCdtTrf>
        <GrpHdr>
            <MsgId>{ref_id}</MsgId>
            <CreDtTm>{timestamp}</CreDtTm>
            <NbOfTxs>1</NbOfTxs>
            <SttlmInf>
                <SttlmMtd>CLRG</SttlmMtd>
            </SttlmInf>
        </GrpHdr>
        <CdtTrfTxInf>
            <IntrBkSttlmAmt Ccy="{currency}">{amount}</IntrBkSttlmAmt>
            <DbtrAgt>
                <FinInstnId>
                    <BICFI>{sender_bic}</BICFI>
                </FinInstnId>
            </DbtrAgt>
            <CdtrAgt>
                <FinInstnId>
                    <BICFI>{recv_bic}</BICFI>
                </FinInstnId>
            </CdtrAgt>
        </CdtTrfTxInf>
    </FIToFICstmrCdtTrf>
</Document>"""
