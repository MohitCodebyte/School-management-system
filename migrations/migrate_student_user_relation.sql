-- Migration: Add user_id foreign key to students table
-- This migration creates a permanent relation between User and Student tables
-- Execute this in MySQL Workbench to fix the student authentication system

USE school_management;

-- Step 1: Add user_id column to students table
ALTER TABLE students
ADD COLUMN user_id INT NULL UNIQUE;

-- Step 2: Add foreign key constraint
ALTER TABLE students
ADD CONSTRAINT fk_student_user
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;

-- Step 3: Link existing student records to user accounts by matching email
-- This will automatically link demo students to their corresponding user accounts
UPDATE students s
JOIN users u ON s.email = u.email
SET s.user_id = u.id
WHERE s.user_id IS NULL;

-- Step 4: Verify the migration
SELECT 
    s.id as student_id,
    s.name as student_name,
    s.email as student_email,
    s.user_id,
    u.id as user_id,
    u.email as user_email,
    u.role as user_role
FROM students s
LEFT JOIN users u ON s.user_id = u.id;
