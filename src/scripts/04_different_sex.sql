-- List of rooms where different-sex students live
SELECT r.id, r.name, count(DISTINCT(s.sex)) as sex_amount
FROM rooms r
JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
HAVING count(DISTINCT(s.sex)) = 2