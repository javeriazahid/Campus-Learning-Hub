USE lms_db;

-- students
INSERT INTO students (full_name, email, phone, enrollment_date, status)
VALUES ('Sheikh Awais Rehman', 'awais.rehman@example.com', '0300-7788991', '2025-01-20', 'Active');

SELECT * FROM students ORDER BY student_id;

SELECT full_name, email, phone FROM students WHERE status = 'Active' ORDER BY full_name;

SELECT student_id, full_name, email FROM students WHERE full_name LIKE '%Khan%' OR email LIKE '%khan%';

UPDATE students SET phone = '0300-1122334', status = 'Inactive' WHERE email = 'awais.rehman@example.com';

DELETE FROM students WHERE email = 'awais.rehman@example.com';

-- instructors
INSERT INTO instructors (full_name, email, specialization, status)
VALUES ('Ms. Hina Rashid', 'hina.rashid@example.com', 'Cyber Security', 'Active');

SELECT * FROM instructors ORDER BY full_name;

UPDATE instructors SET specialization = 'Network Security' WHERE email = 'hina.rashid@example.com';

DELETE FROM instructors WHERE email = 'hina.rashid@example.com';

-- courses
INSERT INTO courses (course_name, description, instructor_id, duration_weeks, fee, status)
VALUES ('Data Structures', 'Arrays, linked lists, stacks, queues and trees', 1, 8, 26000, 'Active');

SELECT c.course_id, c.course_name, i.full_name AS instructor, c.duration_weeks, c.fee, c.status
FROM courses c
INNER JOIN instructors i ON i.instructor_id = c.instructor_id
ORDER BY c.course_name;

UPDATE courses SET fee = 28000, duration_weeks = 10 WHERE course_name = 'Data Structures';

DELETE FROM courses WHERE course_name = 'Data Structures';

-- enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, status)
VALUES (20, 4, '2025-03-01', 'Enrolled');

SELECT s.full_name AS student, c.course_name AS course, e.enrollment_date, e.status
FROM enrollments e
INNER JOIN students s ON s.student_id = e.student_id
INNER JOIN courses c ON c.course_id = e.course_id
ORDER BY e.enrollment_date DESC;

UPDATE enrollments SET status = 'Completed' WHERE student_id = 20 AND course_id = 4;

-- grades
INSERT INTO grades (enrollment_id, assignment_marks, quiz_marks, final_marks)
SELECT enrollment_id, 17, 15, 49 FROM enrollments WHERE student_id = 20 AND course_id = 4;

SELECT s.full_name AS student, c.course_name AS course,
       g.assignment_marks, g.quiz_marks, g.final_marks, g.total_marks
FROM grades g
INNER JOIN enrollments e ON e.enrollment_id = g.enrollment_id
INNER JOIN students s ON s.student_id = e.student_id
INNER JOIN courses c ON c.course_id = e.course_id
ORDER BY g.total_marks DESC;

UPDATE grades SET final_marks = 52
WHERE enrollment_id = (SELECT enrollment_id FROM enrollments WHERE student_id = 20 AND course_id = 4);

DELETE FROM enrollments WHERE student_id = 20 AND course_id = 4;

-- BR-01 courses with the most students
SELECT c.course_name, COUNT(e.enrollment_id) AS enrolled_students
FROM courses c
INNER JOIN enrollments e ON e.course_id = c.course_id
WHERE e.status <> 'Dropped'
GROUP BY c.course_id, c.course_name
ORDER BY enrolled_students DESC;

-- BR-02 courses per instructor
SELECT i.full_name AS instructor, COUNT(c.course_id) AS courses_taught
FROM instructors i
LEFT JOIN courses c ON c.instructor_id = i.instructor_id
GROUP BY i.instructor_id, i.full_name
ORDER BY courses_taught DESC, i.full_name;

-- BR-03 students with the highest total marks
SELECT s.full_name AS student, SUM(g.total_marks) AS total_marks,
       ROUND(SUM(g.total_marks) / COUNT(g.grade_id), 1) AS average_per_course
FROM students s
INNER JOIN enrollments e ON e.student_id = s.student_id
INNER JOIN grades g ON g.enrollment_id = e.enrollment_id
GROUP BY s.student_id, s.full_name
ORDER BY total_marks DESC
LIMIT 10;

-- BR-04 active students
SELECT COUNT(*) AS active_students FROM students WHERE status = 'Active';

-- BR-05 enrollments by status
SELECT status, COUNT(*) AS total FROM enrollments GROUP BY status ORDER BY total DESC;

-- BR-06 courses without students
SELECT c.course_id, c.course_name
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.course_id
WHERE e.enrollment_id IS NULL;

-- instructor workload
SELECT i.full_name AS instructor,
       COUNT(DISTINCT c.course_id) AS courses,
       COUNT(e.enrollment_id) AS students_taught
FROM instructors i
LEFT JOIN courses c ON c.instructor_id = i.instructor_id
LEFT JOIN enrollments e ON e.course_id = c.course_id AND e.status <> 'Dropped'
GROUP BY i.instructor_id, i.full_name
ORDER BY students_taught DESC;

-- student performance with grade
SELECT s.full_name AS student, c.course_name AS course, g.total_marks,
       CASE
           WHEN g.total_marks >= 85 THEN 'A'
           WHEN g.total_marks >= 70 THEN 'B'
           WHEN g.total_marks >= 55 THEN 'C'
           WHEN g.total_marks >= 40 THEN 'D'
           ELSE 'F'
       END AS grade
FROM grades g
INNER JOIN enrollments e ON e.enrollment_id = g.enrollment_id
INNER JOIN students s ON s.student_id = e.student_id
INNER JOIN courses c ON c.course_id = e.course_id
ORDER BY g.total_marks DESC;

-- fee income per course
SELECT c.course_name, COUNT(e.enrollment_id) AS students, SUM(c.fee) AS total_fee
FROM courses c
INNER JOIN enrollments e ON e.course_id = c.course_id
WHERE e.status <> 'Dropped'
GROUP BY c.course_id, c.course_name
ORDER BY total_fee DESC;
