-- Sample PostgreSQL Queries for XRP-LP-Rebalancer
-- These queries join each table with the snapshots table to see the datetime associated with each entry

-- 1. Price Data Query
-- Sample of price_data with timestamps
SELECT 
    p.id,
    s.timestamp,
    s.snapshot_type,
    p.token_id,
    p.token_symbol,
    p.usd_price
FROM 
    price_data p
JOIN 
    snapshots s ON p.snapshot_id = s.id
ORDER BY 
    s.timestamp DESC
LIMIT 10;

-- 2. AMM Data Query
-- Sample of amm_data with timestamps
SELECT 
    a.id,
    s.timestamp,
    s.snapshot_type,
    a.lp_token,
    a.lp_issuer,
    a.lp_token_amount,
    a.asset1,
    a.asset1_issuer,
    a.asset1_amount,
    a.asset1_frozen,
    a.asset2,
    a.asset2_issuer,
    a.asset2_amount,
    a.asset2_frozen
FROM 
    amm_data a
JOIN 
    snapshots s ON a.snapshot_id = s.id
ORDER BY 
    s.timestamp DESC
LIMIT 10;

-- 3. Balance Data Query
-- Sample of balance_data with timestamps
SELECT 
    b.id,
    s.timestamp,
    s.snapshot_type,
    b.address,
    b.token_type,
    b.token_issuer,
    b.balance,
    b.usd_value
FROM 
    balance_data b
JOIN 
    snapshots s ON b.snapshot_id = s.id
ORDER BY 
    s.timestamp DESC
LIMIT 10;

-- 4. LP Position Data Query
-- Sample of lp_position_data with timestamps
SELECT 
    lp.id,
    s.timestamp,
    s.snapshot_type,
    lp.address,
    lp.lp_token,
    lp.lp_issuer,
    lp.lp_token_amount,
    lp.ownership_percentage,
    lp.asset1_amount,
    lp.asset2_amount,
    lp.total_usd_value
FROM 
    lp_position_data lp
JOIN 
    snapshots s ON lp.snapshot_id = s.id
ORDER BY 
    s.timestamp DESC
LIMIT 10;

-- 5. Query for Specific Snapshot Types
-- Filter by snapshot_type
SELECT 
    p.id,
    s.timestamp,
    s.snapshot_type,
    p.token_id,
    p.token_symbol,
    p.usd_price
FROM 
    price_data p
JOIN 
    snapshots s ON p.snapshot_id = s.id
WHERE 
    s.snapshot_type = 'daily'  -- Change to your desired snapshot_type
ORDER BY 
    s.timestamp DESC
LIMIT 10;

-- 6. Query for a Specific Date Range
-- Filter by date range
SELECT 
    b.id,
    s.timestamp,
    s.snapshot_type,
    b.address,
    b.token_type,
    b.balance,
    b.usd_value
FROM 
    balance_data b
JOIN 
    snapshots s ON b.snapshot_id = s.id
WHERE 
    s.timestamp BETWEEN '2023-01-01' AND '2023-01-31'
ORDER BY 
    s.timestamp DESC
LIMIT 10;

-- 7. Query for a Specific Address
-- Filter by address
SELECT 
    lp.id,
    s.timestamp,
    s.snapshot_type,
    lp.address,
    lp.lp_token,
    lp.lp_token_amount,
    lp.ownership_percentage,
    lp.total_usd_value
FROM 
    lp_position_data lp
JOIN 
    snapshots s ON lp.snapshot_id = s.id
WHERE 
    lp.address = 'your_xrp_address_here'
ORDER BY 
    s.timestamp DESC
LIMIT 10;
