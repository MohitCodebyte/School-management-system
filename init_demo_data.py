"""
Demo Data Initialization Script
This script creates demo users for Admin, Teacher, and Student roles if they don't exist.
Run this script to initialize the demo data.
"""

from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

def init_demo_data():
    """Initialize demo users if they don't exist"""
    
    app = create_app('development')
    
    demo_users = [
        {
            'name': 'Admin User',
            'email': 'admin@school.com',
            'password': '123456',
            'role': 'admin'
        },
        {
            'name': 'Teacher User',
            'email': 'teacher@school.com',
            'password': '123456',
            'role': 'teacher'
        },
        {
            'name': 'Student User',
            'email': 'student@school.com',
            'password': '123456',
            'role': 'student'
        }
    ]
    
    with app.app_context():
        try:
            # First, run migration to ensure schema is correct
            print("Checking database schema...")
            try:
                # Check if name column exists
                inspector = db.inspect(db.engine)
                columns = [col['name'] for col in inspector.get_columns('users')]
                
                if 'name' not in columns:
                    print("Adding 'name' column to users table...")
                    with db.engine.connect() as conn:
                        conn.execute(db.text("ALTER TABLE users ADD COLUMN name VARCHAR(255) NOT NULL DEFAULT '' AFTER id"))
                        conn.commit()
                    print("[OK] 'name' column added.")
                
                if 'is_active' not in columns:
                    print("Adding 'is_active' column to users table...")
                    with db.engine.connect() as conn:
                        conn.execute(db.text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE AFTER role"))
                        conn.commit()
                    print("[OK] 'is_active' column added.")
                
                # Update existing users with default names
                with db.engine.connect() as conn:
                    conn.execute(db.text("UPDATE users SET name = CONCAT('User_', id) WHERE name = '' OR name IS NULL"))
                    conn.commit()
                
                print("[OK] Database schema is up to date.")
            except Exception as e:
                print(f"Warning: Schema check failed: {e}")
                print("Continuing with demo data creation...")
            
            for demo_user in demo_users:
                # Check if user already exists
                existing_user = User.query.filter_by(email=demo_user['email']).first()
                
                if existing_user:
                    print(f"User {demo_user['email']} already exists. Skipping...")
                    continue
                
                # Create new user
                user = User(
                    name=demo_user['name'],
                    email=demo_user['email'],
                    role=demo_user['role'],
                    is_active=True
                )
                user.set_password(demo_user['password'])
                
                db.session.add(user)
                db.session.commit()
                
                print(f"Created demo user: {demo_user['email']} ({demo_user['role']})")
            
            print("\nDemo data initialization complete!")
            print("\nDemo Credentials:")
            print("Admin: admin@school.com / 123456")
            print("Teacher: teacher@school.com / 123456")
            print("Student: student@school.com / 123456")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing demo data: {e}")
            raise

if __name__ == '__main__':
    init_demo_data()
