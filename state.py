from typing import Dict, Any, List, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

# 1. The Target Enterprise Data Contract
class ContractSchema(BaseModel):
    vendor_name: str = Field(description="Official legal name of the vendor or contracting party.")
    payment_terms: str = Field(description="Net payment terms, e.g., Net 30, Net 60, Net 90.")
    total_value: float = Field(description="Total extracted financial/monetary contract value. Numeric only.")
    governing_law: str = Field(description="Jurisdiction governing the contract, e.g., New York, California.")
    discrepancies_found: Optional[List[str]] = Field(default=[], description="List of internal document contradictions noted by the extractor.")

# 2. The Shared Stateful Memory Structure
class AuditState(TypedDict):
    raw_document_path: str        # Local system path to the temporary PDF file
    extracted_data: Optional[Dict[str, Any]]
    validation_errors: List[str]
    validation_attempts: int
    requires_human_review: bool
    confidence_score: float
    final_report_path: Optional[str]
