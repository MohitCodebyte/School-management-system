-- Migration Script: Add missing columns to users table
-- This script adds the 'name' and 'is_active' columns to the users table
-- Run this script to fix the schema mismatch error

USE school_management_db;

-- Check if 'name' column exists, if not add it
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'school_management_db' 
AND TABLE_NAME = 'users' 
AND COLUMN_NAME = 'name';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE users ADD COLUMN name VARCHAR(255) NOT NULL DEFAULT '' AFTER id',
    'SELECT ''Column name already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Check if 'is_active' column exists, if not add it
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'school_management_db' 
AND TABLE_NAME = 'users' 
AND COLUMN_NAME = 'is_active';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE AFTER role',
    'SELECT ''Column is_active already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Update existing users to have a default name if name is empty
UPDATE users SET name = CONCAT('User_', id) WHERE name = '' OR name IS NULL;

-- Display current schema
SELECT 'Current users table schema:' AS message;
DESCRIBE users;
