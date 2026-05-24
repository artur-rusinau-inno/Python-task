-- 5 rooms with the largest difference in the age of students
SELECT r.id, r.name, EXTRACT(YEAR FROM (MAX(AGE(s.birthday)) - MIN(AGE(s.birthday)))) as age_diff
FROM rooms r
JOIN students s ON s.room = r.id
GROUP BY r.id, r.name
ORDER BY age_diff DESC
LIMIT 5