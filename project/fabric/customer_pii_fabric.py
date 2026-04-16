from datetime import date
import os
from model.customer import CustomerPII, TaxIdType, CustomerPII_DTO
from model.customerDTO import CustomerPII_DTO

from service.kms_service import generate_blind_index, encrypt, decrypt


data = "123.456.789-01".encode()    # str -> bytes
key_enc = os.urandom(32)            # AES-256 
key_mac = os.urandom(32)            # HMAC
aad = "user_123".encode()           # Additional Authenticated Data (AAD)

email = "email@example.com".encode()
phone = "879123456789".encode()
name = "John Doe".encode()
date_of_birth = date(2003, 8, 29)


customer = CustomerPII(

    tax_id_type=TaxIdType.CPF,
    tax_id_enc=encrypt(data, key_enc, aad),
    tax_id_blind_index=generate_blind_index(key_mac, data),
    tax_id_country='BR',
    key_version_id=1,
    email_enc=encrypt(email, key_enc, aad),
    email_blind_index=generate_blind_index(key_mac, email),
    phone_enc=encrypt(phone, key_enc, aad),
    full_name_enc=encrypt(name, key_enc, aad),
    date_of_birth=date_of_birth
)

def create_customer_pii():
    return customer

def create_customer_pii_DTO(tax_id_type: str, tax_id_value: str, tax_id_country: str, email: str, phone: str, full_name: str, date_of_birth: str) -> CustomerPII:
    return CustomerPII_DTO(
        tax_id_type=tax_id_type,
        tax_id_enc=tax_id_value,
        tax_id_country=tax_id_country,
        key_version_id="1",
        email_enc=email,
        phone_enc=phone,
        full_name_enc=full_name,
        date_of_birth=date_of_birth
    )

def create_customer_pii_DTO_from_customer(customer: CustomerPII) -> CustomerPII_DTO:
    return CustomerPII_DTO(
        tax_id_type=customer.tax_id_type.value,
        tax_id_enc=customer.tax_id_enc.hex(),
        tax_id_country=customer.tax_id_country,
        key_version_id=str(customer.key_version_id),
        email_enc=customer.email_enc.hex(),
        phone_enc=customer.phone_enc.hex(),
        full_name_enc=customer.full_name_enc.hex(),
        date_of_birth=customer.date_of_birth.isoformat()
    )

def create_customer_pii_from_dto(dto: CustomerPII_DTO) -> CustomerPII:

    key_enc = "key_enc".encode()            # AES-256 
    key_mac = "key_mac".encode()          # HMAC
    aad = "user_1".encode() 
    data = dto.tax_id_enc.encode()
    email = dto.email_enc.encode()
    phone = dto.phone_enc.encode()
    name = dto.full_name_enc.encode()
    
    return CustomerPII(
        tax_id_type=TaxIdType(dto.tax_id_type),
        tax_id_enc=encrypt(data, key_enc, aad),
        tax_id_blind_index=generate_blind_index(key_mac, data),  # Blind index não é armazenado no DTO
        tax_id_country=dto.tax_id_country,
        key_version_id=int(dto.key_version_id),
        email_enc=encrypt(email, key_enc, aad),
        email_blind_index=generate_blind_index(key_mac, email),  # Blind index não é armazenado no DTO
        phone_enc=encrypt(phone, key_enc, aad),
        full_name_enc=encrypt(name, key_enc, aad),
        date_of_birth=date.fromisoformat(dto.date_of_birth)
    )
