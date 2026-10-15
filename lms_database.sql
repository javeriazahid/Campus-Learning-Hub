DROP DATABASE IF EXISTS lms_db;
CREATE DATABASE lms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lms_db;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    enrollment_date DATE NOT NULL,
    status ENUM('Active', 'Inactive', 'Graduated') NOT NULL DEFAULT 'Active'
);

CREATE TABLE instructors (
    instructor_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    specialization VARCHAR(100) NOT NULL,
    status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active'
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    instructor_id INT NOT NULL,
    duration_weeks INT NOT NULL CHECK (duration_weeks > 0),
    fee DECIMAL(10, 2) NOT NULL CHECK (fee >= 0),
    status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active',
    FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id)
);

CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    status ENUM('Enrolled', 'Completed', 'Dropped') NOT NULL DEFAULT 'Enrolled',
    UNIQUE (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses (course_id)
);

CREATE TABLE grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_id INT NOT NULL UNIQUE,
    assignment_marks DECIMAL(5, 2) NOT NULL CHECK (assignment_marks BETWEEN 0 AND 20),
    quiz_marks DECIMAL(5, 2) NOT NULL CHECK (quiz_marks BETWEEN 0 AND 20),
    final_marks DECIMAL(5, 2) NOT NULL CHECK (final_marks BETWEEN 0 AND 60),
    total_marks DECIMAL(6, 2) GENERATED ALWAYS AS (assignment_marks + quiz_marks + final_marks) STORED,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments (enrollment_id) ON DELETE CASCADE
);

INSERT INTO students (full_name, email, phone, enrollment_date, status) VALUES
    ('Ahmed Raza', 'ahmed.raza@example.com', '0300-4127731', '2024-01-15', 'Active'),
    ('Fatima Zahra', 'fatima.zahra@example.com', '0321-8836420', '2024-01-15', 'Active'),
    ('Muhammad Usman', 'muhammad.usman@example.com', '0333-5209174', '2024-02-05', 'Active'),
    ('Ayesha Siddiqui', 'ayesha.siddiqui@example.com', '0345-1186092', '2024-02-05', 'Active'),
    ('Hassan Ali', 'hassan.ali@example.com', '0312-7743058', '2024-02-19', 'Active'),
    ('Zainab Fatima', 'zainab.fatima@example.com', '0301-9920647', '2024-03-04', 'Active'),
    ('Bilal Ahmad', 'bilal.ahmad@example.com', '0322-6615839', '2024-03-04', 'Active'),
    ('Hira Nawaz', 'hira.nawaz@example.com', '0336-3074518', '2024-03-18', 'Active'),
    ('Usman Ghani', 'usman.ghani@example.com', '0300-2258764', '2024-04-01', 'Graduated'),
    ('Maryam Khan', 'maryam.khan@example.com', '0344-8102937', '2024-04-01', 'Active'),
    ('Ali Hamza', 'ali.hamza@example.com', '0313-5547206', '2024-04-15', 'Active'),
    ('Sana Javed', 'sana.javed@example.com', '0302-7391825', '2024-05-06', 'Active'),
    ('Saad Mehmood', 'saad.mehmood@example.com', '0331-4680291', '2024-05-06', 'Active'),
    ('Noor Fatima', 'noor.fatima@example.com', '0346-2975113', '2024-05-20', 'Active'),
    ('Hamza Tariq', 'hamza.tariq@example.com', '0323-1869470', '2024-06-03', 'Inactive'),
    ('Iqra Aslam', 'iqra.aslam@example.com', '0315-9038642', '2024-06-03', 'Active'),
    ('Faisal Mahmood', 'faisal.mahmood@example.com', '0334-7421956', '2024-06-17', 'Graduated'),
    ('Rabia Anwar', 'rabia.anwar@example.com', '0303-6150328', '2024-07-01', 'Active'),
    ('Talha Hussain', 'talha.hussain@example.com', '0347-3318094', '2024-07-01', 'Inactive'),
    ('Mehwish Iqbal', 'mehwish.iqbal@example.com', '0324-5826701', '2024-07-15', 'Active');

INSERT INTO instructors (full_name, email, specialization, status) VALUES
    ('Dr. Imran Shah', 'imran.shah@example.com', 'Machine Learning and Python', 'Active'),
    ('Ms. Sadia Malik', 'sadia.malik@example.com', 'Databases and Data Analysis', 'Active'),
    ('Mr. Kamran Akbar', 'kamran.akbar@example.com', 'Web and Cloud Technologies', 'Active'),
    ('Dr. Nadia Hussain', 'nadia.hussain@example.com', 'Digital Marketing', 'Active'),
    ('Mr. Tariq Mehmood', 'tariq.mehmood@example.com', 'Graphic Design', 'Active');

INSERT INTO courses (course_name, description, instructor_id, duration_weeks, fee, status) VALUES
    ('Python Programming', 'Core Python from variables to functions and file handling', 1, 8, 25000, 'Active'),
    ('MySQL Database Design', 'Relational design, SQL queries, joins and constraints', 2, 6, 22000, 'Active'),
    ('Data Analysis with Pandas', 'Cleaning, grouping and visualising data with Pandas', 2, 6, 28000, 'Active'),
    ('Machine Learning Fundamentals', 'Regression, classification and model evaluation with scikit-learn', 1, 10, 45000, 'Active'),
    ('Web Development Basics', 'HTML, CSS and a first look at Python web apps', 3, 8, 30000, 'Active'),
    ('Digital Marketing', 'Social media, SEO and campaign analytics', 4, 5, 18000, 'Active'),
    ('Cloud Computing Basics', 'Cloud concepts, virtual machines and storage', 3, 6, 35000, 'Inactive');

INSERT INTO enrollments (student_id, course_id, enrollment_date, status) VALUES
    (1, 1, '2025-02-06', 'Enrolled'),
    (2, 1, '2025-03-07', 'Enrolled'),
    (3, 1, '2025-04-08', 'Completed'),
    (4, 1, '2025-05-09', 'Enrolled'),
    (1, 2, '2025-06-10', 'Enrolled'),
    (5, 1, '2025-07-11', 'Completed'),
    (2, 2, '2025-08-12', 'Dropped'),
    (6, 1, '2025-09-13', 'Enrolled'),
    (7, 1, '2025-01-14', 'Completed'),
    (4, 2, '2025-02-15', 'Enrolled'),
    (8, 1, '2025-03-16', 'Enrolled'),
    (2, 3, '2025-04-17', 'Completed'),
    (9, 1, '2025-05-18', 'Enrolled'),
    (6, 2, '2025-06-19', 'Dropped'),
    (10, 1, '2025-07-20', 'Completed'),
    (11, 1, '2025-08-21', 'Enrolled'),
    (8, 2, '2025-09-22', 'Enrolled'),
    (5, 3, '2025-01-23', 'Completed'),
    (12, 1, '2025-02-24', 'Enrolled'),
    (3, 4, '2025-03-05', 'Enrolled'),
    (10, 2, '2025-04-06', 'Dropped'),
    (7, 3, '2025-05-07', 'Enrolled'),
    (13, 2, '2025-06-08', 'Enrolled'),
    (14, 2, '2025-07-09', 'Completed'),
    (15, 2, '2025-08-10', 'Enrolled'),
    (9, 4, '2025-09-11', 'Enrolled'),
    (13, 3, '2025-01-12', 'Completed'),
    (16, 3, '2025-02-13', 'Dropped'),
    (17, 3, '2025-03-14', 'Enrolled'),
    (11, 5, '2025-04-15', 'Completed'),
    (12, 5, '2025-05-16', 'Enrolled'),
    (16, 4, '2025-06-17', 'Enrolled'),
    (18, 4, '2025-07-18', 'Completed'),
    (14, 6, '2025-08-19', 'Enrolled'),
    (15, 6, '2025-09-20', 'Dropped'),
    (19, 5, '2025-01-21', 'Completed'),
    (20, 5, '2025-02-22', 'Enrolled');

INSERT INTO grades (enrollment_id, assignment_marks, quiz_marks, final_marks) VALUES
    (1, 19, 10, 48),
    (2, 18, 11, 44),
    (3, 11, 14, 40),
    (4, 20, 12, 30),
    (5, 17, 15, 31),
    (6, 11, 10, 52),
    (8, 14, 15, 31),
    (9, 17, 9, 47),
    (10, 11, 17, 44),
    (11, 12, 12, 52),
    (12, 14, 9, 50),
    (13, 14, 19, 40),
    (15, 18, 14, 44),
    (16, 11, 18, 31),
    (17, 19, 12, 34),
    (18, 12, 12, 47),
    (19, 11, 10, 53),
    (20, 13, 17, 39),
    (22, 12, 18, 42),
    (23, 15, 16, 54),
    (24, 20, 11, 54),
    (25, 16, 17, 42),
    (26, 19, 16, 40),
    (27, 12, 20, 46),
    (29, 17, 19, 56),
    (30, 20, 9, 52),
    (31, 16, 18, 54),
    (32, 14, 14, 35),
    (33, 19, 17, 47),
    (34, 15, 11, 55),
    (36, 15, 14, 37),
    (37, 16, 10, 45);
