import asyncio
import asyncpg

from fabric.customer_pii_fabric import create_customer_pii, create_customer_pii_DTO, create_customer_pii_from_dto

cDTO = create_customer_pii_DTO(  # chama sua função
    tax_id_type="CPF",
    tax_id_value="123.456.789-01",
    tax_id_country="BR",
    email="email@example.com",
    phone="879123456789",
    full_name="John Doe",
    date_of_birth="2003-08-29"
)

c = create_customer_pii_from_dto(cDTO)  # converte para CustomerPII

async def main():
    conn = await asyncpg.connect('postgresql://postgres:root@localhost:5432/lab_dados')

    query = '''
    INSERT INTO access.customers_pii(
        tax_id_type,
        tax_id_enc,
        tax_id_blind_index,
        tax_id_country,
        key_version_id,
        email_enc,
        email_blind_index,
        phone_enc,
        full_name_enc,
        date_of_birth
    )
    VALUES(
        $1,  -- tax_id_type
        $2,  -- tax_id_enc
        $3,  -- tax_id_blind_index
        $4,  -- tax_id_country
        $5,  -- key_version_id
        $6,  -- email_enc
        $7,  -- email_blind_index
        $8,  -- phone_enc
        $9,  -- full_name_enc
        $10  -- date_of_birth
    )
    RETURNING customer_id;
    '''

    params = (
        c.tax_id_type,        # $1
        c.tax_id_enc,         # $2
        c.tax_id_blind_index, # $3
        c.tax_id_country,     # $4
        c.key_version_id,     # $5
        c.email_enc,          # $6
        c.email_blind_index,  # $7
        c.phone_enc,          # $8
        c.full_name_enc,      # $9
        c.date_of_birth       # $10                      
    )

    customer_id = await conn.fetchval(query, *params)
    print("Inserted customer_id:", customer_id)

    await conn.close()

asyncio.run(main())

# Insert(Query(CriarQuery(Customer)), Conexão)
