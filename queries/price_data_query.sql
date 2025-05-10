-- Price Data Query
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
