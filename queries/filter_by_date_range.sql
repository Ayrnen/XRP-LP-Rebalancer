-- Query for a Specific Date Range
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
