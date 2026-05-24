-- SQL query that adds the required indexes
CREATE INDEX idx_student_room ON students (room) -- для join между students и rooms
CREATE INDEX idx_age ON students (birthday) -- часто делаем AGE(student.birthday)