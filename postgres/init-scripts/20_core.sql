CREATE TABLE IF NOT EXISTS core.policies(
    policy_version_id UUID PRIMARY KEY DEFAULT uuidv7(),
    -- surrogate key 
    policy_number VARCHAR(36) NOT NULL,
    -- natural key 
    policy_id UUID NOT NULL,
    -- surrogate key for logical FK relationships
    version_id BIGINT DEFAULT 1,
    customer_id UUID NOT NULL REFERENCES access.customers_pii(customer_id),
    meta_region VARCHAR(2),
    product_code VARCHAR(50),
    policy_status varchar(20) CHECK (
        policy_status IN (
            'ACTIVE',
            'CANCELLED',
            'PENDING',
            'EXPIRED',
            'OTHER'
        )
    ),
    validity_period tstzrange NOT NULL,
    risk_attributes JSONB,
    CONSTRAINT unique_policy_version UNIQUE (policy_id, version_id),
    EXCLUDE USING GIST (
        policy_number WITH =,
        validity_period WITH &&
    ) WITH (fillfactor = 95)
);

CREATE TABLE IF NOT EXISTS core.policy_operations (
    idempotency_key UUID PRIMARY KEY,
    -- operation-level idempotency key
    policy_version_id UUID REFERENCES core.policies(policy_version_id),
    -- logical FK 
    operation_type TEXT NOT NULL CHECK (operation_type IN ('create', 'update', 'delete')),
    STATUS TEXT NOT NULL CHECK (STATUS IN ('pending', 'completed', 'failed')),
    response_body JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS core.policy_coverages(
    coverage_id UUID PRIMARY KEY DEFAULT uuidv7(),
    -- surrogate key
    policy_id UUID NOT NULL,
    --fk logical
    policy_version_id UUID NOT NULL REFERENCES core.policies(policy_version_id),
    version_id BIGINT DEFAULT 1,
    coverage_type VARCHAR(50) NOT NULL,
    -- natural key
    limit_amount DECIMAL(15, 2) NOT NULL,
    deductible_amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    retroactive DATE,
    tailcoverage DATE,
    meta_region varchar(2),
    validity_period tstzrange NOT NULL,
    EXCLUDE USING GIST (
        policy_id WITH =,
        coverage_type WITH =,
        validity_period WITH &&
    )
);

CREATE TABLE IF NOT EXISTS core.policy_documents (
    document_id UUID PRIMARY KEY DEFAULT uuidv7(),
    -- surrogate key
    policy_id UUID NOT NULL,
    coverage_id UUID NULL,
    doc_name VARCHAR(255) NOT NULL,
    -- natural key
    doc_storage_path VARCHAR(500) NOT NULL,
    -- operation key
    doc_type VARCHAR(20) NOT NULL CHECK (
        doc_type IN (
            'POLICY',
            'ENDORSEMENT',
            'CLAIM',
            'INVOICE',
            'OTHER'
        )
    ),
    version_id BIGINT DEFAULT 1,
    meta_region VARCHAR(2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ NULL,
    upload_by UUID NOT NULL REFERENCES system.actors(actor_id),
    CHECK (
        (coverage_id IS NULL)
        OR (coverage_id IS NOT NULL)
    )
);