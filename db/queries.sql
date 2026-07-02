-- afisam cele mai noi rulari
SELECT * FROM runs ORDER BY run_date DESC;

-- afisam coverpoints unei rulari specifice si acoperirea lora
SELECT name, coverage FROM coverpoints
WHERE run_id = 1;

-- cate bin-uri miss are o rulare
SELECT COUNT(*) AS miss_bins
FROM runs r
JOIN coverpoints c on c.run_id = r.id
JOIN bins b        on b.coverpoint_id = c.id
where r.id = 1 and b.hit = 0
