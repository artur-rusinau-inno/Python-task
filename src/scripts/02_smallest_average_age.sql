-- 5 rooms with the smallest average age of students
SELECT r.id, r.name, EXTRACT(YEAR FROM AVG(AGE(s.birthday))) as avg_age
FROM rooms r
JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
ORDER BY avg_age ASC
LIMIT 5