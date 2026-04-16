from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID

@dataclass(frozen=True)
class CustomerPII_DTO:
    tax_id_type: str
    tax_id_enc: str
    tax_id_country: str 
    key_version_id: str
    email_enc: str
    phone_enc: str
    full_name_enc: str
    date_of_birth: str
    
    # Campos com valor default ou gerados pelo banco
    customer_id: Optional[UUID] = None,
    tax_id_blind_index = None,
    email_blind_index = None,
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None