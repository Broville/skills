---
name: postgresql
description: PostgreSQL schema design — data types, constraints, indexing, partitioning, JSONB, generated columns, extensions, and safe schema evolution
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - Designing a schema for PostgreSQL
  - Selecting data types and constraints
  - Planning indexes, partitions, or RLS policies
  - Reviewing tables for scale and maintainability
  - Migrating or evolving a PostgreSQL schema
related_skills:
  - api-security-best-practices
  - deployment-procedures
---

# PostgreSQL

## Description

A comprehensive reference for PostgreSQL-specific schema design. Covers data types, constraints, indexing, partitioning, JSONB, generated columns, extensions, and safe schema evolution. Includes connection security notes for production deployments.

## When to Use

- Designing a schema for PostgreSQL
- Selecting data types and constraints
- Planning indexes, partitions, or RLS policies
- Reviewing tables for scale and maintainability
- Migrating or evolving a schema

## When NOT to Use

- Targeting a non-PostgreSQL database
- Only needing query tuning without schema changes
- Needing a database-agnostic modeling guide

## Connection Security

When connecting to PostgreSQL in production:

1. **Use SSL/TLS** — Always enforce SSL for remote connections:
   ```
   host all all 0.0.0.0/0 md5
   hostssl all all 0.0.0.0/0 md5
   ```
2. **Never hardcode credentials** — Use environment variables or secret managers:
   ```bash
   export PGHOST=db.example.com
   export PGDATABASE=myapp
   export PGUSER=app_user
   export PGPASSWORD=$(cat /run/secrets/pg_password)
   ```
3. **Principle of least privilege** — Create application-specific roles with minimal permissions:
   ```sql
   CREATE ROLE app_readonly LOGIN PASSWORD 'secure_password';
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;
   ```
4. **Use connection pooling** — Configure PgBouncer or use built-in connection pooling (PG16+) to limit connections.

## Core Rules

- Define a **PRIMARY KEY** for reference tables. Prefer `BIGINT GENERATED ALWAYS AS IDENTITY`; use `UUID` only when global uniqueness/opacity is needed.
- **Normalize first (to 3NF)** to eliminate data redundancy; denormalize **only** for measured, high-ROI reads where join performance is proven problematic.
- Add **NOT NULL** everywhere it's semantically required; use **DEFAULT**s for common values.
- Create **indexes for access paths you actually query**: PK/unique (auto), **FK columns (manual!)**, frequent filters/sorts, and join keys.
- Prefer **TIMESTAMPTZ** for event time; **NUMERIC** for money; **TEXT** for strings; **BIGINT** for integer values; **DOUBLE PRECISION** for floats (or `NUMERIC` for exact decimal arithmetic).

## PostgreSQL Gotchas

- **Identifiers**: Unquoted → lowercased. Avoid quoted/mixed-case names. Convention: `snake_case`.
- **Unique + NULLs**: UNIQUE allows multiple NULLs. Use `UNIQUE (...) NULLS NOT DISTINCT` (PG15+) to restrict to one NULL.
- **FK indexes**: PostgreSQL does NOT auto-index FK columns. Add them manually.
- **No silent coercions**: Length/precision overflows error out (no truncation).
- **Sequences/identity have gaps**: Normal behavior — don't try to make IDs consecutive.
- **Heap storage**: No clustered PK by default. `CLUSTER` is one-off reorganization, not maintained.
- **MVCC**: Updates/deletes leave dead tuples; vacuum handles them. Design to avoid hot wide-row churn.

## Data Types

### IDs
```sql
-- Preferred for most tables
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY

-- For distributed systems or opaque IDs
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
-- PG18+ preferred: DEFAULT uuidv7()
```

### Strings
Prefer `TEXT`. If length limits needed, use `CHECK (LENGTH(col) <= n)` instead of `VARCHAR(n)`. Avoid `CHAR(n)`.

Case-insensitive: use expression indexes on `LOWER(col)` (preferred) or `CITEXT`.

Large strings (>2KB threshold) automatically stored in TOAST with compression.

### Money
```sql
price NUMERIC(10,2) NOT NULL CHECK (price > 0)
```
Never use `FLOAT` or `REAL` for money. Use `NUMERIC(p,s)`.

### Time
```sql
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
```
- Use `TIMESTAMPTZ`, never `TIMESTAMP` (without timezone).
- Never use `TIMESTAMPTZ(0)` or any precision specification.
- `now()` for transaction start time, `clock_timestamp()` for current wall-clock time.
- Never use `TIMETZ`.

### Booleans
```sql
is_active BOOLEAN NOT NULL DEFAULT true
```

### Enums
```sql
-- For small, stable sets
CREATE TYPE order_status AS ENUM ('PENDING', 'PAID', 'CANCELED');

-- For evolving business values, use TEXT + CHECK or lookup table
status TEXT NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'PAID', 'CANCELED'))
```

### Arrays
```sql
tags TEXT[] NOT NULL DEFAULT '{}'
-- Index with GIN for containment (@>), overlap (&&)
```

### Ranges
```sql
booking_period TSTZRANGE NOT NULL
-- Index with GiST. Use [) (inclusive/exclusive) bounds by default.
```

### JSONB
```sql
attrs JSONB NOT NULL DEFAULT '{}'
-- Index with GIN: CREATE INDEX ON tbl USING GIN (attrs);
-- Prefer JSONB over JSON (always).
-- Use ONLY for optional/semi-structured attributes.
-- Keep core relations in normal columns.
```

### Text Search
```sql
-- Always specify language
CREATE INDEX ON tbl USING GIN (to_tsvector('english', content));
-- Query with:
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'search terms')
-- Never use single-argument to_tsvector or to_tsquery.
```

### Do NOT Use
- `timestamp` (without TZ) — use `timestamptz`
- `char(n)` or `varchar(n)` — use `text` with `CHECK`
- `money` type — use `numeric`
- `timetz` — use `timestamptz`
- `serial` — use `generated always as identity`

## Constraints

```sql
-- Primary Key (auto-creates B-tree index)
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY

-- Foreign Key with explicit actions
user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE

-- Unique (allows multiple NULLs unless NULLS NOT DISTINCT)
email TEXT NOT NULL UNIQUE

-- Composite unique with single NULL
UNIQUE (company_id, email) NULLS NOT DISTINCT

-- Check constraint
price NUMERIC NOT NULL CHECK (price > 0)

-- Exclusion constraint (prevent overlapping bookings)
EXCLUDE USING gist (room_id WITH =, booking_period WITH &&)
```

**FK tip**: Always add explicit index on FK columns. Use `DEFERRABLE INITIALLY DEFERRED` for circular FK dependencies.

## Indexing

```sql
-- B-tree (default): equality, range, ORDER BY
CREATE INDEX ON orders (user_id);
CREATE INDEX ON orders (created_at);

-- Composite: order matters
CREATE INDEX ON orders (user_id, created_at);
-- WHERE user_id = ? AND created_at > ? uses index
-- WHERE created_at = ? does NOT use this index

-- Covering: index-only scan
CREATE INDEX ON orders (user_id) INCLUDE (status, total);

-- Partial: hot subsets
CREATE INDEX ON orders (user_id) WHERE status = 'active';

-- Expression: computed keys
CREATE INDEX ON users (LOWER(email));

-- GIN: JSONB, arrays, text search
CREATE INDEX ON profiles USING GIN (attrs);
CREATE INDEX ON users USING GIN (to_tsvector('english', name));
-- Heavy @> workloads: jsonb_path_ops (smaller, but no key-existence queries)
CREATE INDEX ON profiles USING GIN (attrs jsonb_path_ops);

-- GiST: ranges, geometry, exclusion
-- BRIN: very large, naturally ordered data (time-series)
```

## Partitioning

For very large tables (>100M rows) where queries consistently filter on the partition key:

```sql
-- Range partitioning (time-series)
CREATE TABLE logs (
  id BIGINT GENERATED ALWAYS AS IDENTITY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  message TEXT NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE logs_2024_01 PARTITION OF logs
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- List partitioning (regions)
CREATE TABLE events PARTITION BY LIST (region);
CREATE TABLE events_us PARTITION OF events FOR VALUES IN ('us-east', 'us-west');

-- Hash partitioning (even distribution)
CREATE TABLE metrics PARTITION BY HASH (user_id);
```

**Limitations**: No global UNIQUE constraints — include partition key in PK/UNIQUE. FKs from partitioned tables not supported.

## Generated Columns

```sql
-- STORED: computed on write, indexable
ALTER TABLE orders ADD COLUMN total_with_tax NUMERIC
  GENERATED ALWAYS AS (total * 1.1) STORED;

-- PG18+: VIRTUAL (computed on read, not stored)
-- ALTER TABLE orders ADD COLUMN total_with_tax NUMERIC
--   GENERATED ALWAYS AS (total * 1.1) VIRTUAL;
```

## Extensions

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;    -- crypt() for password hashing
CREATE EXTENSION IF NOT EXISTS pg_trgm;     -- Fuzzy text search, LIKE '%pattern%'
CREATE EXTENSION IF NOT EXISTS citext;      -- Case-insensitive text type
CREATE EXTENSION IF NOT EXISTS btree_gin;   -- Mixed GIN indexes
CREATE EXTENSION IF NOT EXISTS timescaledb; -- Time-series automation (3rd party)
CREATE EXTENSION IF NOT EXISTS postgis;     -- Geospatial (3rd party)
CREATE EXTENSION IF NOT EXISTS vector;      -- pgvector for embeddings (3rd party)
```

## Safe Schema Evolution

```sql
-- Concurrent index creation (doesn't block writes)
CREATE INDEX CONCURRENTLY ON orders (user_id);

-- Safe column addition with non-volatile default
ALTER TABLE orders ADD COLUMN status TEXT NOT NULL DEFAULT 'PENDING';
-- NOTE: volatile defaults (now(), gen_random_uuid()) rewrite entire table

-- Drop constraints before columns
ALTER TABLE orders DROP CONSTRAINT orders_status_check;
ALTER TABLE orders DROP COLUMN status;

-- Transactional DDL (most DDL can run in transactions)
BEGIN;
ALTER TABLE orders ADD COLUMN priority INT;
-- Test the change
ROLLBACK;  -- or COMMIT;
```

## Example: Users and Orders

```sql
CREATE TABLE users (
  user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email TEXT NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX ON users (LOWER(email));
CREATE INDEX ON users (created_at);

CREATE TABLE orders (
  order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(user_id),
  status TEXT NOT NULL DEFAULT 'PENDING'
    CHECK (status IN ('PENDING', 'PAID', 'CANCELED')),
  total NUMERIC(10,2) NOT NULL CHECK (total > 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ON orders (user_id);
CREATE INDEX ON orders (created_at);

CREATE TABLE profiles (
  user_id BIGINT PRIMARY KEY REFERENCES users(user_id),
  attrs JSONB NOT NULL DEFAULT '{}',
  theme TEXT GENERATED ALWAYS AS (attrs->>'theme') STORED
);
CREATE INDEX profiles_attrs_gin ON profiles USING GIN (attrs);
```

## Pitfalls

1. **Missing FK indexes** — PostgreSQL does NOT auto-create indexes on FK columns. Without them, deletes on the parent table lock the entire child table. Always add: `CREATE INDEX ON orders (user_id);`
2. **Using `VARCHAR(n)` instead of `TEXT`** — `VARCHAR(n)` adds a length check but no performance benefit. Use `TEXT` with `CHECK (LENGTH(col) <= n)` if you need a limit.
3. **Using `TIMESTAMP` instead of `TIMESTAMPTZ`** — `TIMESTAMP` without timezone causes data corruption when servers or clients are in different timezones. Always use `TIMESTAMPTZ`.
4. **Using `SERIAL` instead of `IDENTITY`** — `SERIAL` has permission gaps and is not SQL-standard. Use `BIGINT GENERATED ALWAYS AS IDENTITY`.
5. **Adding `NOT NULL` columns with volatile defaults** — `ALTER TABLE ADD COLUMN col TIMESTAMPTZ NOT NULL DEFAULT now()` rewrites the entire table. Add as nullable first, backfill, then add `NOT NULL`.

## Verification

1. **Schema is valid:**
   ```bash
   psql -c "\dt+ my_table"    # Table exists with expected columns
   psql -c "\d my_table"      # Verify columns, types, constraints, indexes
   ```
2. **Indexes exist on FK columns:**
   ```sql
   SELECT conrelid::regclass AS table, conname AS fk_constraint,
          a.attname AS fk_column
   FROM pg_constraint c
   JOIN pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
   WHERE contype = 'f'
   AND NOT EXISTS (
     SELECT 1 FROM pg_index i
     WHERE i.indrelid = c.conrelid
     AND a.attnum = ANY(i.indkey)
   );
   -- Should return no rows (all FKs indexed)
   ```
3. **Migration runs without locking:**
   ```sql
   -- Test in transaction, then rollback
   BEGIN;
   CREATE INDEX CONCURRENTLY ON my_table (my_column);  -- Note: can't run in transaction
   ROLLBACK;
   -- Use CREATE INDEX CONCURRENTLY outside transactions
   ```