CREATE TABLE access.customers_pii (
    customer_id UUID PRIMARY KEY DEFAULT uuidv7(),
    -- surrogate key
    tax_id_type VARCHAR(20) NOT NULL CHECK (tax_id_type IN ('SSN', 'CPF', 'VAT', 'OTHER')),
    tax_id_enc BYTEA NOT NULL,
    tax_id_blind_index VARCHAR(64) NOT NULL,
    -- natural key for lookups
    tax_id_country VARCHAR(2) NOT NULL,
    key_version_id INT NOT NULL,
    email_enc BYTEA NOT NULL,
    email_blind_index VARCHAR(64),
    -- natural key for lookups
    phone_enc BYTEA NOT NULL,
    full_name_enc BYTEA NOT NULL,
    date_of_birth DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ NULL CHECK (char_length(tax_id_country) = 2),
    CHECK (
        date_of_birth < CURRENT_DATE
        AND date_of_birth > '1900-01-01'
    ),
    CHECK (key_version_id > 0),
    CHECK (
        deleted_at IS NULL
        OR deleted_at >= created_at
    ),
    CHECK (updated_at >= created_at)
);

CREATE TABLE access.customer_pii_operations (
    idempotency_key UUID PRIMARY KEY,
    customer_id UUID REFERENCES access.customers_pii(customer_id),
    operation_type TEXT NOT NULL CHECK (operation_type IN ('create', 'update', 'delete')),
    STATUS TEXT NOT NULL CHECK (STATUS IN ('pending', 'completed', 'failed')),
    response_body JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE UNIQUE INDEX uq_customer_tax_identity ON access.customers_pii (tax_id_blind_index, tax_id_type, tax_id_country)
WHERE
    deleted_at IS NULL;

CREATE UNIQUE INDEX uq_customer_email_active ON access.customers_pii (email_blind_index)
WHERE
    deleted_at IS NULL
    AND email_blind_index IS NOT NULL;