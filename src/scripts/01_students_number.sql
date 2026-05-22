-- List of rooms and the number of students in each of them
SELECT r.id, r.name, COUNT(s.id)
FROM rooms r
JOIN students s on r.id = s.room
GROUP BY r.id, r.name