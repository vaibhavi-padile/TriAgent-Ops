import os
import json
import urllib.request
from typing import Dict, Any
from pypdf import PdfReader  # Clean, zero-cost multi-page PDF reader
from google import genai
from google.genai import types
from dotenv import load_dotenv
from state import ContractSchema, AuditState

# Initialize system configuration variables safely
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_key)

class OperationsAgents:
    
    def extractor_agent(self, state: AuditState) -> Dict[str, Any]:
        """Agent 1: Extract structure data from a multi-page binary PDF file."""
        print("🤖 [Extractor Agent] Ingesting and reading PDF structure...")
        
        pdf_path = state["raw_document_path"]
        compiled_text = ""
        
        try:
            # Dynamically read and loop through all pages of the uploaded PDF
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            print(f"📄 [PDF Engine] Detected {total_pages} total document pages. Parsing layout...")
            
            for index, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    compiled_text += f"\n--- PAGE {index + 1} ---\n{page_text}"
        except Exception as e:
            print(f"❌ [PDF Engine Error] Failed to extract text layer from PDF: {e}")
            compiled_text = "ERROR: Failed to process document layout structure."

        # Re-inject previous system notes if the Validator rejects the data
        error_context = ""
        if state["validation_errors"]:
            error_context = f"\nPREVIOUS SYSTEM VALIDATION ERRORS TO RESOLVE:\n" + "\n".join(state["validation_errors"])

        system_prompt = (
            "You are a Senior Corporate Operations Intelligent Extraction Agent. "
            "Your core task is to extract specified fields from the multi-page document raw text context. "
            "Examine all available data fields carefully, paying special attention to financial values, tables, and signature blocks. "
            "If exact data fields are missing, note that in discrepancies or use deep contextual inference." + error_context
        )

        # Enforce structured JSON payloads out of multi-page data layers
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Multi-Page Document Raw Text Content:\n{compiled_text}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=ContractSchema,
            ),
        )
        
        extracted_dict = json.loads(response.text)
        
        return {
            "extracted_data": extracted_dict,
            "validation_attempts": state.get("validation_attempts", 0) + 1
        }

    def validator_agent(self, state: AuditState) -> Dict[str, Any]:
        """Agent 2: Cross-checks data parameters against strict enterprise policies."""
        print("🔍 [Validator Agent] Validating extracted data contracts...")
        data = state["extracted_data"] or {}
        errors = []
        confidence = 1.0

        if data.get("total_value", 0) <= 0:
            errors.append("Total value parameter cannot be equal to or less than 0.")
            confidence -= 0.4

        approved_vendors = ["Acme Corp", "Globex Industries", "Initech LLC", "Stark Industries"]
        if data.get("vendor_name") not in approved_vendors:
            errors.append(f"Vendor '{data.get('vendor_name')}' is unauthorized or absent from the corporate ERP ledger.")
            confidence -= 0.3

        if "Net 90" in data.get("payment_terms", ""):
            errors.append("Net 90 conditions violate standard corporate cash-flow rules.")
            confidence -= 0.2

        requires_human = confidence < 0.8 and state["validation_attempts"] >= 2

        return {
            "validation_errors": errors,
            "confidence_score": max(0.0, confidence),
            "requires_human_review": requires_human
        }

    def reporter_agent(self, state: AuditState) -> Dict[str, Any]:
        """Agent 3: Processes operational briefs and fires clean webhooks."""
        print("📊 [Reporter Agent] Generating actionable outputs...")
        data = state["extracted_data"] or {}
        errors = state["validation_errors"]
        
        is_flagged = len(errors) > 0 or state["requires_human_review"]
        status_text = "⚠️ FLAGGED FOR SYSTEM AUDIT" if is_flagged else "✅ APPROVED FOR ERP DATABASE WRITES"
        
        report_content = f"""# Operations Audit Report
**Status:** {status_text}
**Confidence Score:** {state.get('confidence_score', 0.0) * 100:.0f}%

## System Ingestion Data Metrics
- **Vendor Label:** {data.get('vendor_name', 'N/A')}
- **Payment Structure:** {data.get('payment_terms', 'N/A')}
- **Contract Asset Allocation:** ${data.get('total_value', 0):,.2f}
"""
        output_file = "operations_audit_report.md"
        with open(output_file, "w") as f:
            f.write(report_content)

        webhook_url = os.getenv("OPERATIONS_WEBHOOK_URL")
        
        if is_flagged and webhook_url:
            print("🚀 [Reporter Agent] High-priority issue found! Dispatching webhook alert...")
            violations_list = "\n".join([f"• {err}" for err in errors])
            message_text = (
                f"🚨 *OpsIntel Alert: Document Validation Failure* 🚨\n"
                f"*Vendor:* {data.get('vendor_name', 'Unknown')}\n"
                f"*Pipeline Score:* {state.get('confidence_score', 0.0) * 100:.0f}%\n"
                f"*Flagged Contradictions:* \n{violations_list}\n\n"
                f"👉 *Action Required:* Review dashboard metadata outputs."
            )
            
            webhook_payload = {"text": message_text, "content": message_text}
            
            try:
                req = urllib.request.Request(
                    webhook_url,
                    data=json.dumps(webhook_payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req) as response:
                    if 200 <= response.status < 300:
                        print("✅ [Webhook Engine] Telemetry broadcast completed successfully!")
            except Exception as e:
                print(f"❌ [Webhook Error] Direct communication routing failed: {e}")

        return {"final_report_path": output_file}
