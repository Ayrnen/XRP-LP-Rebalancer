-- Balance Data Query
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
