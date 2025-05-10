-- Query for Specific Snapshot Types
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
