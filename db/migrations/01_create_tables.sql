-- Create snapshots table
CREATE TABLE IF NOT EXISTS snapshots (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    snapshot_type TEXT NOT NULL
);

-- Create price_data table
CREATE TABLE IF NOT EXISTS price_data (
    id SERIAL PRIMARY KEY,
    snapshot_id INTEGER NOT NULL,
    token_id TEXT NOT NULL,
    token_symbol TEXT NOT NULL,
    usd_price REAL NOT NULL,
    FOREIGN KEY (snapshot_id) REFERENCES snapshots (id)
);

-- Create amm_data table
CREATE TABLE IF NOT EXISTS amm_data (
    id SERIAL PRIMARY KEY,
    snapshot_id INTEGER NOT NULL,
    lp_token TEXT NOT NULL,
    lp_issuer TEXT NOT NULL,
    lp_token_amount REAL NOT NULL,
    asset1 TEXT NOT NULL,
    asset1_issuer TEXT,
    asset2 TEXT NOT NULL,
    asset1_amount REAL NOT NULL,
    asset1_frozen BOOLEAN,
    asset2_issuer TEXT NOT NULL,
    asset2_amount REAL NOT NULL,
    asset2_frozen BOOLEAN,
    FOREIGN KEY (snapshot_id) REFERENCES snapshots (id)
);

-- Create balance_data table
CREATE TABLE IF NOT EXISTS balance_data (
    id SERIAL PRIMARY KEY,
    snapshot_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    token_type TEXT NOT NULL,
    token_issuer TEXT,
    balance REAL NOT NULL,
    usd_value REAL,
    FOREIGN KEY (snapshot_id) REFERENCES snapshots (id)
);

-- Create lp_position_data table
CREATE TABLE IF NOT EXISTS lp_position_data (
    id SERIAL PRIMARY KEY,
    snapshot_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    lp_token TEXT NOT NULL,
    lp_issuer TEXT NOT NULL,
    lp_token_amount REAL NOT NULL,
    ownership_percentage REAL NOT NULL,
    asset1_amount REAL NOT NULL,
    asset2_amount REAL NOT NULL,
    total_usd_value REAL,
    FOREIGN KEY (snapshot_id) REFERENCES snapshots (id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_price_data_snapshot_id ON price_data(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_amm_data_snapshot_id ON amm_data(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_balance_data_snapshot_id ON balance_data(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_lp_position_data_snapshot_id ON lp_position_data(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_balance_data_address ON balance_data(address);
CREATE INDEX IF NOT EXISTS idx_lp_position_data_address ON lp_position_data(address);