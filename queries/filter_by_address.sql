-- Query for a Specific Address
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
