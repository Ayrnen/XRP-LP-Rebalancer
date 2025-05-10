-- LP Position Data Query
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
