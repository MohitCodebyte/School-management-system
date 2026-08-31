"""
Database Migration Script
This script runs the SQL migration to add missing columns to the users table.
Run this script to fix the schema mismatch error.
"""

import pymysql
from config import Config

def run_migration():
    """Execute the migration SQL to add missing columns"""
    
    try:
        # Connect to MySQL database
        connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("Connected to database successfully.")
        
        with connection.cursor() as cursor:
            # Check if 'name' column exists
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'name'
            """, (Config.DB_NAME,))
            name_exists = cursor.fetchone()['count'] > 0
            
            if not name_exists:
                print("Adding 'name' column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN name VARCHAR(255) NOT NULL DEFAULT '' AFTER id")
                print("[OK] 'name' column added successfully.")
            else:
                print("[OK] 'name' column already exists.")
            
            # Check if 'is_active' column exists
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'is_active'
            """, (Config.DB_NAME,))
            is_active_exists = cursor.fetchone()['count'] > 0
            
            if not is_active_exists:
                print("Adding 'is_active' column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE AFTER role")
                print("[OK] 'is_active' column added successfully.")
            else:
                print("[OK] 'is_active' column already exists.")
            
            # Update existing users to have a default name if name is empty
            cursor.execute("UPDATE users SET name = CONCAT('User_', id) WHERE name = '' OR name IS NULL")
            print("[OK] Updated existing users with default names.")
            
            # Check and fix role ENUM if it has 'staff' instead of 'student'
            cursor.execute("""
                SELECT COLUMN_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'role'
            """, (Config.DB_NAME,))
            result = cursor.fetchone()
            
            if result and 'staff' in result['COLUMN_TYPE']:
                print("Fixing role ENUM (changing 'staff' to 'student')...")
                # First, update any users with 'staff' role to 'student'
                cursor.execute("UPDATE users SET role = 'student' WHERE role = 'staff'")
                # Then modify the ENUM definition
                cursor.execute("ALTER TABLE users MODIFY COLUMN role ENUM('admin', 'teacher', 'student') NOT NULL DEFAULT 'admin'")
                print("[OK] Role ENUM fixed.")
            
            # Commit changes
            connection.commit()
            print("\n[SUCCESS] Migration completed successfully!")
            
            # Display current schema
            print("\nCurrent users table schema:")
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            for column in columns:
                print(f"  - {column['Field']}: {column['Type']}")
            
    except Exception as e:
        print(f"Error during migration: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            connection.close()
            print("\nDatabase connection closed.")

if __name__ == '__main__':
    print("=" * 60)
    print("Database Migration Script")
    print("=" * 60)
    print()
    run_migration()
