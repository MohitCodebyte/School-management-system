-- Migration: Add user_id foreign key to students table
-- This migration creates a permanent relation between User and Student tables

-- Add user_id column to students table
ALTER TABLE students
ADD COLUMN user_id INT UNIQUE;

-- Add foreign key constraint
ALTER TABLE students
ADD CONSTRAINT fk_student_user
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;

-- Link existing demo student records by matching email
UPDATE students s
JOIN users u ON s.email = u.email
SET s.user_id = u.id
WHERE s.user_id IS NULL;
