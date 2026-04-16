CREATE TABLE IF NOT EXISTS system.actors (
    actor_id UUID PRIMARY KEY DEFAULT uuidv7(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NULL,
    role VARCHAR(20) NOT NULL CHECK (
        role IN (
            'ANALYST',
            'MANAGER',
            'AUDITOR',
            'SERVICE',
            'ADMIN'
        )
    ),
    actor_type VARCHAR(20) NOT NULL CHECK (actor_type IN ('HUMAN', 'SERVICE', 'SYSTEM')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ NULL
);

CREATE TABLE system.transactionaal_outbox (
    event_id UUID NOT NULL DEFAULT uuidv7(),
    correlation_id UUID NOT NULL,
    aggregate_type VARCHAR(50) NOT NULL,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    region_code VARCHAR(5) NOT NULL,
    PRIMARY KEY (event_id)
)