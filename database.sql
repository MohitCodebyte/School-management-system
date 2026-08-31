-- School Management System Database Schema
-- Database Name: school_management_db

CREATE DATABASE IF NOT EXISTS school_management_db;
USE school_management_db;

-- Users Table (for authentication)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'teacher', 'student') DEFAULT 'admin',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admission_number VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    class VARCHAR(50) NOT NULL,
    section VARCHAR(10),
    parent_name VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    admission_date DATE,
    photo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Teachers Table
CREATE TABLE IF NOT EXISTS teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(255),
    qualification VARCHAR(255),
    experience INT,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    joining_date DATE,
    photo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Classes Table
CREATE TABLE IF NOT EXISTS classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(50) NOT NULL,
    section VARCHAR(10),
    class_teacher_id INT,
    room_number VARCHAR(20),
    capacity INT,
    FOREIGN KEY (class_teacher_id) REFERENCES teachers(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    class_id INT,
    date DATE NOT NULL,
    status ENUM('Present', 'Absent', 'Late') DEFAULT 'Present',
    remarks TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_attendance (student_id, date)
);

-- Fees Table
CREATE TABLE IF NOT EXISTS fees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    fee_type VARCHAR(100) NOT NULL,
    total_fee DECIMAL(10, 2) NOT NULL,
    paid_fee DECIMAL(10, 2) DEFAULT 0.00,
    due_fee DECIMAL(10, 2) NOT NULL,
    payment_date DATE,
    payment_method VARCHAR(50),
    status ENUM('Paid', 'Pending', 'Partial') DEFAULT 'Pending',
    academic_year VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Exams Table
CREATE TABLE IF NOT EXISTS exams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exam_name VARCHAR(255) NOT NULL,
    student_id INT NOT NULL,
    subject VARCHAR(255) NOT NULL,
    marks_obtained DECIMAL(5, 2),
    total_marks DECIMAL(5, 2) NOT NULL,
    grade VARCHAR(10),
    exam_date DATE,
    academic_year VARCHAR(20),
    remarks TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Notices Table
CREATE TABLE IF NOT EXISTS notices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    target_audience ENUM('All', 'Students', 'Teachers', 'Parents') DEFAULT 'All',
    priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Notifications Table (New centralized notification system)
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_by INT NOT NULL,
    sender_role ENUM('admin', 'teacher', 'student') NOT NULL,
    target_role ENUM('admin', 'teacher', 'student', 'all') NOT NULL,
    target_class VARCHAR(50),
    target_section VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    is_pinned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert Sample Data

-- Insert Demo Users (with hashed passwords - these are plain text for demo, should be hashed in production)
INSERT INTO users (name, email, password, role, is_active) VALUES 
('Admin User', 'admin@school.com', '123456', 'admin', TRUE),
('Teacher User', 'teacher@school.com', '123456', 'teacher', TRUE),
('Student User', 'student@school.com', '123456', 'student', TRUE);

-- Insert Sample Teachers
INSERT INTO teachers (name, subject, qualification, experience, phone, email, address, date_of_birth, gender, joining_date) VALUES 
('Dr. Sarah Anderson', 'Mathematics', 'Ph.D. Mathematics', 15, '9876543220', 'sarah.anderson@school.com', '111 Teacher Lane, City', '1980-03-15', 'Female', '2010-06-01'),
('Mr. Michael Thompson', 'Physics', 'M.Sc. Physics', 12, '9876543221', 'michael.thompson@school.com', '222 Educator Road, City', '1982-07-20', 'Male', '2012-06-01'),
('Mrs. Emily White', 'English', 'M.A. English', 10, '9876543222', 'emily.white@school.com', '333 Professor Street, City', '1985-11-10', 'Female', '2014-06-01');

-- Insert Sample Students
INSERT INTO students (admission_number, name, class, section, parent_name, phone, email, address, date_of_birth, gender, admission_date) VALUES 
('ADM001', 'John Smith', '10', 'A', 'Robert Smith', '9876543210', 'john.smith@email.com', '123 Main Street, City', '2008-05-15', 'Male', '2020-04-01'),
('ADM002', 'Emma Johnson', '10', 'A', 'Michael Johnson', '9876543211', 'emma.johnson@email.com', '456 Oak Avenue, City', '2008-08-20', 'Female', '2020-04-01'),
('ADM003', 'William Brown', '10', 'B', 'James Brown', '9876543212', 'william.brown@email.com', '789 Pine Road, City', '2008-03-10', 'Male', '2020-04-01'),
('ADM004', 'Sophia Davis', '9', 'A', 'David Davis', '9876543213', 'sophia.davis@email.com', '321 Elm Street, City', '2009-07-25', 'Female', '2021-04-01'),
('ADM005', 'James Wilson', '9', 'B', 'Thomas Wilson', '9876543214', 'james.wilson@email.com', '654 Maple Drive, City', '2009-11-30', 'Male', '2021-04-01');

-- Insert Sample Classes
INSERT INTO classes (class_name, section, class_teacher_id, room_number, capacity) VALUES 
('10', 'A', 1, '101', 40),
('10', 'B', 2, '102', 40),
('9', 'A', 3, '103', 40),
('9', 'B', 1, '104', 40),
('8', 'A', 2, '105', 35),
('8', 'B', 3, '106', 35);

-- Insert Sample Attendance
INSERT INTO attendance (student_id, class_id, date, status) VALUES 
(1, 1, CURDATE(), 'Present'),
(2, 1, CURDATE(), 'Present'),
(3, 2, CURDATE(), 'Absent'),
(4, 3, CURDATE(), 'Present'),
(5, 4, CURDATE(), 'Present');

-- Insert Sample Fees
INSERT INTO fees (student_id, fee_type, total_fee, paid_fee, due_fee, payment_date, payment_method, status, academic_year) VALUES 
(1, 'Tuition Fee', 50000.00, 50000.00, 0.00, '2024-04-15', 'Bank Transfer', 'Paid', '2024-25'),
(2, 'Tuition Fee', 50000.00, 30000.00, 20000.00, '2024-04-20', 'Cash', 'Partial', '2024-25'),
(3, 'Tuition Fee', 50000.00, 0.00, 50000.00, NULL, NULL, 'Pending', '2024-25'),
(4, 'Tuition Fee', 45000.00, 45000.00, 0.00, '2024-04-10', 'Bank Transfer', 'Paid', '2024-25'),
(5, 'Tuition Fee', 45000.00, 20000.00, 25000.00, '2024-04-25', 'Cheque', 'Partial', '2024-25');

-- Insert Sample Exams
INSERT INTO exams (exam_name, student_id, subject, marks_obtained, total_marks, grade, exam_date, academic_year) VALUES 
('Mid-Term Exam', 1, 'Mathematics', 85.00, 100.00, 'A', '2024-10-15', '2024-25'),
('Mid-Term Exam', 1, 'Physics', 78.00, 100.00, 'B+', '2024-10-16', '2024-25'),
('Mid-Term Exam', 2, 'Mathematics', 92.00, 100.00, 'A+', '2024-10-15', '2024-25'),
('Mid-Term Exam', 2, 'English', 88.00, 100.00, 'A', '2024-10-17', '2024-25'),
('Mid-Term Exam', 3, 'Mathematics', 65.00, 100.00, 'C+', '2024-10-15', '2024-25'),
('Mid-Term Exam', 4, 'English', 95.00, 100.00, 'A+', '2024-10-17', '2024-25'),
('Mid-Term Exam', 5, 'Physics', 72.00, 100.00, 'B', '2024-10-16', '2024-25'),
('Final Exam', 1, 'Mathematics', 90.00, 100.00, 'A+', '2024-12-10', '2024-25'),
('Final Exam', 2, 'Mathematics', 88.00, 100.00, 'A', '2024-12-10', '2024-25'),
('Final Exam', 3, 'Physics', 70.00, 100.00, 'B', '2024-12-11', '2024-25');

-- Insert Sample Notices
INSERT INTO notices (title, description, date, target_audience, priority, created_by) VALUES 
('Annual Day Celebration', 'The Annual Day function will be held on 25th December 2024. All students are required to participate.', '2024-12-01', 'All', 'High', 1),
('Winter Break Announcement', 'School will remain closed for winter break from 20th December 2024 to 2nd January 2025.', '2024-12-15', 'All', 'Medium', 1),
('Parent-Teacher Meeting', 'Parent-Teacher meeting for Class 10 students scheduled on 15th December 2024 at 10 AM.', '2024-12-10', 'Parents', 'High', 1),
('Science Exhibition', 'Science exhibition will be organized on 18th December 2024. Interested students should register by 10th December.', '2024-12-05', 'Students', 'Medium', 1),
('Sports Day', 'Annual Sports Day will be conducted on 20th January 2025. Practice sessions will start from 2nd January.', '2024-12-20', 'All', 'Medium', 1);

-- Insert Sample Notifications
INSERT INTO notifications (title, message, created_by, sender_role, target_role, is_pinned) VALUES 
('School Holiday Tomorrow', 'School will remain closed tomorrow due to heavy rain forecast. Stay safe at home.', 1, 'admin', 'all', TRUE),
('Fee Submission Last Date', 'Last date for fee submission is 30th of this month. Please ensure timely payment.', 1, 'admin', 'student', FALSE),
('Mathematics Assignment Due', 'Mathematics assignment submission due tomorrow. Please complete and submit.', 2, 'teacher', 'student', FALSE),
('Parent-Teacher Meeting', 'Parent-Teacher meeting scheduled for next Friday at 10 AM.', 1, 'admin', 'all', FALSE),
('Exam Schedule Released', 'Final exam schedule has been released. Check your dashboard for details.', 1, 'admin', 'student', TRUE);

UPDATE users
SET password='scrypt:32768:8:1$HitQA94LFWVYVzaZ$51e54ef06cce0132ef35af4d1bfc7011fccf4a026aae4b4a88d0e7e20090037a2f96eb4c8409506978470cb2ee6fc8eb257e7f7dbb1e54d6be141311d3d2206b'
WHERE email='admin@school.com';