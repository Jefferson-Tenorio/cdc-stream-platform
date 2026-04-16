from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID

class TaxIdType(str, Enum):
    SSN = "SSN"
    CPF = "CPF"
    VAT = "VAT"
    OTHER = "OTHER"

@dataclass(frozen=True)
class CustomerPII:
    tax_id_type: TaxIdType
    tax_id_enc: bytes
    tax_id_blind_index: bytes
    tax_id_country: str 
    key_version_id: int
    email_enc: bytes
    email_blind_index: bytes
    phone_enc: bytes
    full_name_enc: bytes
    date_of_birth: date
    
    # Campos com valor default ou gerados pelo banco
    customer_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None