-- AMM Data Query
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
