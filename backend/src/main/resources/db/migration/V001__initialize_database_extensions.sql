-- Infrastructure-only migration.
-- Creates the pgvector extension and domain schemas.
-- Does not create product tables.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS identity;
CREATE SCHEMA IF NOT EXISTS scripture;
CREATE SCHEMA IF NOT EXISTS reading;
CREATE SCHEMA IF NOT EXISTS reflection;
CREATE SCHEMA IF NOT EXISTS guidance;
CREATE SCHEMA IF NOT EXISTS understanding;
CREATE SCHEMA IF NOT EXISTS saar;
CREATE SCHEMA IF NOT EXISTS search;
CREATE SCHEMA IF NOT EXISTS platform;
