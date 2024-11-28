DROP TABLE IF EXISTS raw.users;
CREATE TABLE raw.users (
    id numeric(100) NOT NULL,
    username varchar,
    has_access boolean DEFAULT false,
    record_updated_dtt timestamptz DEFAULT CURRENT_TIMESTAMP,
    record_load_dtt timestamptz DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_pk PRIMARY KEY (id)
);
